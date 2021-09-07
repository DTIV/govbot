My submission for GITCOIN Decentralized Governance Hackathon: Build A Governance Bot. 
This is a Discord Gorvernace Explorer Bot that uses keyword commands to retrieve Governance data on different protocols, proposals and voters. Updates User on all active and queued proposals or a specified proposal.

------- SETUP -------

1. Create Discord Server and Create Application
2. Create A Virtual Environment
3. pip install requirements.txt
4. Set .env file using sample_env.txt
5. python discordbot.py

------- COMMANDS -------

GOVBOT COMMANDS

--------------------
/menu : List of commands
/listproto : list of available protocols
--------------------
/active: List of all active proposals
/que: List of all queued proposals
/canceled: List of all canceled proposals
/changed: List of changed proposals that have changed status
--------------------
$(protocol) set : add protocol for updates on active proposals and changes
$(protocol) clear : clear protocol from updates
--------------------
$(protocol) : all data from specified protocol
$(protocol) proposals : lists all proposal titles for protocol
$(protocol) refid : lists all proposal ref IDs
$(protocol) contract : get contract address and network
$(protocol) active : gets all active proposals for specific protocol
$(protocol) que : gets all queued proposals for a specific protocol
$(protocol) canceled : gets all canceled proposals for specific protocol 
--------------------
$(protocol) (title): gets specific proposal data
$(protocol) (ref ID): gets specific proposal data
--------------------

            