import pandas as pd
import matplotlib.pyplot as plt

IP_CLIENT = "192.168.0.3"
FILENAME = 'random.csv'
def makeFinerprint(fname):
  filenameNoExt = fname.split('.')[0]
  df = pd.read_csv("training/"+fname, sep=',')
  # "No.","Time","Source","Destination","Protocol","Length","Info"

  # Da usare solo con il csv di Whireshark, non server con tshark.
  df.drop("Info", axis=1, inplace=True)
  df.drop("No.", axis=1, inplace=True)
  df.drop("Time", axis=1, inplace=True)
  df.drop("Port", axis=1, inplace=True)
  if 'Lenght TC' in df.columns:
    df.drop("Lenght TCP", axis=1, inplace=True)
  # df = df[(df["Protocol"] == "TCP")] # Solo pacchetti TCP

  # Creazione colonna direction
  df["direction"] = df["Destination"].apply(lambda x: "-" if x == IP_CLIENT else "+")

  # Rimozione rumore (pacchetti di dimensione 52 (66))
  # Le richieste da parte del client hanno dimensione 602
  df = df[(df["Length"] != 66)]
  df.reset_index(drop=True, inplace=True) 

  # print(df)

  # Inserimento di un marker ad ogni cambio di direzione con la quantita' 
  # di dati trasmessi in ogni direzione
  prevDir = "+"
  sizeMarker = 0
  sizeMarkers = []
  for idx, row in df.iterrows():
    direction = row["direction"]
    size = row["Length"]
    if direction == prevDir:
      sizeMarker += size
    else:
      df.loc[idx, "S"] = (sizeMarker/610+1)*600
      sizeMarker = size
      prevDir = direction
  # print(df)
  lastSizeMarker = (sizeMarker/610+1)*600
  # df.loc[len(df.index)] = {"S": lastSizeMarker}
  totalSizeMarker = df["S"].sum()

  totalSizeP = df[df["direction"] == "+"]["Length"].sum()
  totalSizeN = df[df["direction"] == "-"]["Length"].sum()
  totalSizeP = ((totalSizeP-1)/10000+1)*10000
  totalSizeN = ((totalSizeN-1)/10000+1)*10000
  # df['TSp'] = df[df["direction"] == "+"]["Length"].cumsum()
  # df['TSn'] = df[df["direction"] == "-"]["Length"].cumsum()

  s = df["S"].iloc[len(df.index)-1]
  # print("S", s)
  # print("TP+", totalSizeP)
  # print("TP+", totalSizeN)

  # Inserimento di un HTML Marker che indica la dimensione della pagina HTML
  # df["htmlMarker"] = df["Length"].apply(lambda x: (x/610+1)*600)
  # Contanto le dimensioni in ingresso tra il primo pacchetto in uscita ed i seguenti pacchetti in uscita,
  # possiamo estrarre la dimensione della pagina HTML.
  #! I pacchetti di lunghezza 602 sono altro rumore???

  primaRigaConRichiestaHTML = df[(df["direction"] == "+") & (df["Length"] > 602)].index[0]
  # print("primaRigaConRichiestaHTML", df[(df["direction"] == "+") & (df["Length"] > 602)])

  htmlFlagStart = 0
  htmlFlagEnd = 0
  htmlMarker = 0
  prevDir = '+'
  for idx, row in df.iterrows():
    direction = row["direction"]
    size = row["Length"]
    if direction == '-' and idx > primaRigaConRichiestaHTML and htmlFlagEnd == 0 and size > 602:
      htmlMarker += size
    elif direction != '-' and idx > primaRigaConRichiestaHTML:
      df.loc[primaRigaConRichiestaHTML, "htmlMarker"] = (htmlMarker/610+1)*600
      htmlFlagEnd = 1

  # print(df)


  # Conteggio dei pacchetti inviati in ogni direzione, 
  # il primo di ogni blocco in ciascuna direzione
  # ha N pari al numero di pacchetti che seguono nella stessa direzione
  n = 1
  index = 0
  prevDir = '+'
  for idx, row in df.iterrows():
    direction = row["direction"]
    if direction == prevDir:
      n += 1
    else:
      df.loc[index, "N"] = n
      prevDir = direction
      index = idx
      n = 1

  uniqueP = df[(df["direction"] == "+")]["Length"].nunique()
  uniqueN = df[(df["direction"] == "-")]["Length"].nunique()
  opNormalized = (((uniqueP-1)/2)+1)*2
  onNormalized = (((uniqueN-1)/2)+1)*2

  # print("OP+", opNormalized)
  # print("OP-", onNormalized)


  nPacketsP = df[(df["direction"] == "+")].count()[0]
  nPacketsN = df[(df["direction"] == "-")].count()[0]
  # print("PP+", nPacketsP)
  # print("PP-", nPacketsN)
  percentPoverN = float(nPacketsP)/nPacketsN 
  percentPoverNNormalized = (float((int(((((percentPoverN-.01)*100))/5)+1)*5))/100)
  # print("PP+/PP-", percentPoverNNormalized)

  npP = (((nPacketsP-1)/15)+1)*15
  npN= (((nPacketsN-1)/15)+1)*15

  # print('NP+', npP)
  # print('NP-', npN)

  # print("Last size markers", str(lastSizeMarker))
  # print("Total size markers", str(totalSizeMarker))

  # print(df)

  rows = 1
  columns = 3
  fig = plt.figure(figsize=(15, 5))

  fig.add_subplot(rows, columns, 1)
  plt.title("Size Markers")
  dfTMP = df.dropna(subset=["S"])
  dfTMP["S"].plot(kind="bar", xticks=[])

  fig.add_subplot(rows, columns, 2)
  plt.title("Number Markers")
  dfTMP = df.dropna(subset=["N"])
  dfTMP["N"].plot(kind="bar", xticks=[])


  fig.add_subplot(rows, columns, 3)
  plt.title("Size and direction")
  dfTMP = df
  dfTMP["L2"] = dfTMP.apply(lambda x: x["Length"] if x["direction"] == "+" else x["Length"] * -1, axis=1)
  dfTMP["L2"].plot(kind="bar", xticks=[])

  plt.savefig(filenameNoExt + "-figure.png")
  # plt.show()
  return (s,totalSizeP,totalSizeN,primaRigaConRichiestaHTML,opNormalized,onNormalized,nPacketsP,nPacketsN,percentPoverNNormalized)


site = ["ansa", "unical", "facebook", "youtube", "archlinux"]
data = []
for i,s in enumerate(site):
  x = makeFinerprint(s+".csv")
  d = {}
  d["site"] = s
  d["S"] = x[0]
  d["TP+"] = x[1]
  d["TP-"] = x[2]
  d["firstHTML"] = x[3]
  d["OP+"] = x[4]
  d["OP-"] = x[5]
  d["PP+"] = x[6]
  d["PP-"] = x[7]
  d["PPperc"] = x[8]
  data.append(d)
print(data)
  