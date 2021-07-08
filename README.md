This is the final draft of analyses which appeared in the *The American Sociologist* [article](https://link.springer.com/article/10.1007%2Fs12108-021-09490-4) I published, "Lost & Forgotten: An Index of the Famous Works Which Sociology Has Left Behind".

The `load_db.py` file fixes the few errors I noticed in the grouping algorithm included in `knowknow`.
Somehow these edits should ship with every use of the dataset, but I have not added this to the API or interface.
For now, you should start every notebook with `from load_db import db`.

To use this package, first install [`knowknow`](https://github.com/amcgail/knowknow), then run:

+ `python -m knowknow clone https://github.com/amcgail/lost-forgotten`
+ `python -m knowknow start lost-forgotten`

When you first access the dataset, your computer will download all count files from Harvard Dataverse, which uses ~750MB of data.
Enjoy, and feel free to [reach out](https://twitter.com/SomeKindOfAlec) with any questions, comments, etc.