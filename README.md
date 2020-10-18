# Anoixo_hebrew
Extension on Anoixo project that process OT

Link to Anoixo project: https://github.com/sheesania/anoixo

I can't upload all the code, so the files here are only those with changes.
Copy the folder `text_provider` to `anoixo/server/anoixo-server/text_providers/`. Copy `STEPBible-Data` to the root folder `anoixo`.

#### How does it work?
Go to `anoixo/server/anoixo-server/text_providers/`, and run `python OT_extract_attributes.py`.
The queries array is hard coded in function `run_test()` at this moment. It is expected to be recevied from user input in the frontend.


