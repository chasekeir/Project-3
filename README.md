# Project-3

<p> The <code>ebay-dl.py</code> file webscrapes the first 10 pages of an ebay search term and returns the name, price, shipping cost, status, if the item has free returns, and how many of the item has been sold. After finding this information, the code will input the data into a <code>json</code> fie or a <code>csv</code> file depending on which one the user wants</p>

### Use of Program

<p> To use the program one must direct their attention to their terminal. after doing so, input this code <code>$ python3 ebay-dl.py 'item name'</code> the item name is whatever you want to search on ebay.</p>

<p> In order to make it a <code>csv</code> file, one must enter another thing to the end of their terminal. This new command will look like <code>$ python3 ebay-dl.py 'item name' --csv=True</code>