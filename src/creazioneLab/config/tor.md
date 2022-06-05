Can I run a tor network?
Tor is open source. There aren't a lot of instructions for actually deploying the Directory Authorities, but what is there is not bad. And you can absolutely run your own tor network. There are actually three different ways to do it. Chutney and shadow are tools designed mostly for setting up test networks for running experiements in labratory conditions. Shadow is specifically designed for running bandwidth tests across large-sized tor networks. So if you want to model a tor network running 50,000 nodes - shadow's your huckleberry.

But if you want to deply an as-authentic tor network as possible, do it manually. It's not all that hard. And if you want to conduct research on tor's protocols, it's a great way to do it safely, instead of actively de-anonymizing real users in the wild. Here are the approxmate steps:

- Configure and compile tor, as normal, on all your boxes.
   - If you're going to run multiple daemons per machine, you may want to use `./configure --prefix=/directory/tor-instance-1` to segment them.
- Start configuring a few Directory Authorities.
   - This step is generating the keys for them and the DirServer lines. Run `tor-gencert` to generate an identity key. Then run `tor --list-fingerprint`. Create your DirServer lines like `DirServer orport=<port> v3ident=<fingerprint from authority_certificate, no spaces> <ip>:<port> <fingerprint from --list-fingerprint in ABCD EF01 format>` These DirServer lines are what put you onto an alternate tor network instead of the official one. You need one line per Directory Authority, and all DirServer lines need to be in the configuration of every DirAuth, Node, and Client you want to talk to this network.
  # pem pashprase testazzo99



- Finish the Directory Authorites configuration.
  - You should set SOCKSPort to 0, ORPort to something, and DirPort to something.
  - You need to set AuthoritativeDirectory and V3AuthoritativeDirectory. You can also set VersioningAuthoritativeDirectory along with RecommendedClientVersions and RecommendedServerVersions - why not. Perhaps you want to copy ConsensusParams out of a recent consensus, also. If you're going to run multiple tor daemons off a single IP address, you should set AuthDirMaxServersPerAddr 0 (0 is unlimited, default is two servers per IP.)
  - You will also (probably) want to lower the voting times, so you can generate a consensus quicker. I'd suggest, to start off with, V3AuthVotingInterval 5 minutes, V3AuthVoteDelay 30 seconds, and V3AuthDistDelay 30 seconds . You can also set MinUptimeHidServDirectoryV2 to something like 1 hour.

- Start up your Directory Authorities.
  - They should all be running, and you should see stuff like 'Time to vote' and 'Uploaded a vote to...' in the notices.log
  - You will also see Nobody has voted on the Running flag. Generating and publishing a consensus without Running nodes would make many clients stop working. Not generating a consensus! This is normal. If TestingAuthDirTimeToLearnReachability is not set (and it's not) - a Directory Authority will wait 30 minutes before voting to consider a relay to be Running. You should either wait 30 minutes and be patient, or set AssumeReachable to skip the 30 minute wait. They will shortly begin generating a consensus you can see at `http://<ip>:<port>/tor/status-vote/current/consensus`

- Start adding more nodes.
  - Configure some Exit and Relay nodes (and optionally Bridges). For each node, you will need to put the DirServer lines. If you're running your nodes in the same /16, you will also need to set EnforceDistinctSubnets 0.
  - There is one other thing you will need to set for the first few nodes though: AssumeReachable 1. This is because if the consensus has no Exit Nodes, a subtle bug will manifest, and nodes will get in a loop and will not upload their descriptors to the Directory Authorities for inclusion in the consensus. By setting AssumeReachable, we skip the test. (The other option is to set up one of your Directory Authorities as an Exit node.)

- Run Depictor.
  - Depictor is a service that monitors the Directory Authorities and generates a pretty website that will give you a lot of info about your network. (Full disclosure, I wrote depictor, cutting over an older java-based tool called 'Doctor' to python)
  
At this point, you can add those DirServer lines to some clients and start sending traffic through your network. The only hard thing left is soliciting hundreds to thousands of relay operators to see the value in splitting from the official network to join yours. =)