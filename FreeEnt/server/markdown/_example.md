To check out the documentation for Python-Markdown [go here](https://python-markdown.github.io/). By default, I've included the following extensions:

* [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/) to allow adding id, classes, and attributes to your markdown. This is enabled, but nothing is using it currently. A fantastic tool for more customization than I'm supplying out of the box.
* [Definition Lists](https://python-markdown.github.io/extensions/definition_lists/) to provide an alternative to using unorderd and ordered lists. testing adding a bunch more text to see if it wraps or not automatically
* [Tables](https://python-markdown.github.io/extensions/tables/) to provide support for tabular information.
* [Admonitions](https://python-markdown.github.io/extensions/admonition/) provides support for call outs

Any markdown files you plan to use for this documentation, including the documentation markdown, can be viewed by saving the file in the `FreeEnt/server/markdown` folder, and then navigating to `/markdown_test?md_file=your_file_name`. If you leave the query string parameter (`?md_file=your_file_name`) off, you'll get this documentation file.

# Basic Markdown (this is an H1)

## Here's an h2

### H3 is the final header I've styled

Here is an example of **Bold Text**. Here is some _italicized text_.

### Admonitions 

Admonitions are great call outs to surface/reinforce a key point, whether it be a warning, informational note, or someting else. They have a syntax where the first line functions as the title and selecting what type of admonition you'll use, and afterwards anything else you want in the admonition needs to be indented a tab's worth of space (and follow normal markdown indentation rules after that). The first line looks like:

`!!! warning "Your Title"`

The currently supported list of types you can use are:
* warning
* info
* danger

!!! warn "Warning Title"
    Indent to keep things within the admonition

    here's a second paragraph

    * you can do lists
    * with things and stuff

!!! info "Good Info Here!"
    Here's the first bit of good news! Dr. Farnsworth has done it again.

### Definiton Lists: 
A definition list is fairly similar an unordered list with a `list-style-type` of `none`, and adding this into the markdown lets you have a version like that, while still keeping bulleted lists as an option. The syntax has each list item start with a colon and then a tab at the beginning. 

Rosa
:   has aim
:   learns cure3, cure4, and life2 before the heat death of the universe. This is nearly forever, ya know?
:   learns bersk a little later, learns exit only after defeating Zot
:   This is an example of a definition list


## Tables
To show an example of a table, here you go:

First Header  | Second Header | Third Header 
------------- | ------------- | ---
Content Cell  | Content Cell  | Content
Content Cell  | Content Cell  | Content


## Attribute Lists
Using the Attribute Lists extension isn't something I've implemented in this first pass, and it's more to help do some significant customization. Go back to the top of the document for a link to the documentation for how it works.