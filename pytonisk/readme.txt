



Network Service
===============

Puts messages in the outgoing queue and reads the incoming queue.

API
---

Provides the SEND function for its subscribers/users and invokes the
callback ON_MESSAGE.


Broadcast Service
=================

Contains a list of hosts, subscribes to the Network Service.

API
---

Provides the BROADCAST function, invokes the ON_BROADCAST function of its
users.

vessel.handle_message()
  broadcast.on_message()
  consensus.on_broadcast()
  leader_election.on_decision()

network.handle_message()
  broadcast.on_message()
    consensus.on_broadcast()
      leader_election.on_decision()
        consensus.decide()
          broadcast.cast()
            network.send()
