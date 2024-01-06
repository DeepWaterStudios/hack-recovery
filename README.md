# Anti-bot scripts for lost private keys

I first posted about this here: https://twitter.com/twitt_tr/status/1741525416467161409

This repo contains some scripts you can use to fund a wallet after having lost the private key, when a bot is watching
to auto drain any incoming gas.

This won't work on more advanced bots, but the same principles can be applied, I think. A really good bot that uses a
validator will probably be unbeatable though.

The `rescue_avax.py` script contains the basic 'fund the wallet' script, and `rescue_wavax.py` was a script I used to
recover funds being extracted from the hyperspace airdrop.

For instructions on usage see each individual script.

Repo probably looks a bit weird because I just chipped out the relevant parts of a private python web3 toolkit I use for
small projects like this. I'm not fixing it.
