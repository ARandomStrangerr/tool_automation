# `MLClassification.py`
## Goal
For a given invoice, the goal of this file is to:
* Pick out the name of the vendor (the other company, not the one that you are working at).
* Pick out the total amount of the invoice.
* Based on the content of the invoice, decide what kind of spending code that this invoice belong to.

## Picking Company for the Invoice
The implement method is `Conditional Random Field` (CRF). It is good for `structured prediction`. Why? because an invoice is structured, invoice from one vendor looks similar to another (typical name somewher around the begining, close to "to" or "from", company name contains "ltd", "llc", or "inc" and some other features).

For the implementation:
* Split text into tokens.
* Label the tokens (I use [Label Studio](#"https://labelstud.io/guide/install.html")). I export the file to JSON, import into label-studio, export to another JSON, read back into the code).
* Add features into tokens
* Using CRF and fit with the data (train). You can also export the model if the model is good enough for you.
* Using the trained model to predict new invoice (repeat step 1 and 3).
Typically, we given the CRF variable x (tokens) and predict its variable y (label).

As you can see, common use case for CRF involves when we can give each token its context and guessing its label based on its context:
* Named Entity Recognition: Extracting entities (like company's name).
* Part-of-Speech Tagging: Assigning grammatical roles to words in a sentence.
* Chunking: Grouping related words in a sentence.

Strength:
* Context Awareness: CRF consider the relationship among its neighbour labels.
* Feature Engineering: you can modifine / define features of each token if you think that it is important.

### How Does the Mathematics Work?
