# Anoixo hebrew edition

#### About this work
Extension on Anoixo project that processes OT.

Link to Anoixo project: https://github.com/sheesania/anoixo

I can't upload all the code, so the files here are only those with changes.
You will need to first clone the original Anoixo project. 
Then copy the folder `text_provider` in this repo to `anoixo/server/anoixo-server/text_providers/`. Copy `STEPBible-Data` to the root folder `anoixo/`.

#### How does it work?
Go to `anoixo/server/anoixo-server/text_providers/`, and run `python OT_extract_attributes.py`. 
The query input is currently hard coded in the function `run_test()` at this moment. (feel free to change anything for testing)
It is expected to receive queries from user input at the frontend.

#### Contact
For any technique question, please contact bunny_sung@yahoo.com.hk
