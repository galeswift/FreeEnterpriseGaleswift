[TOC]

To check out the documentation for Python-Markdown [go here](https://python-markdown.github.io/). By default, I've included the following extensions:

* [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/) to allow adding id, classes, and attributes to your markdown. This is enabled, but nothing is using it currently. A fantastic tool for more customization than I'm supplying out of the box.
* [Definition Lists](https://python-markdown.github.io/extensions/definition_lists/) to provide an alternative to using unorderd and ordered lists. testing adding a bunch more text to see if it wraps or not automatically
* [Tables](https://python-markdown.github.io/extensions/tables/) to provide support for tabular information.
* [Table of Contents](https://python-markdown.github.io/extensions/toc) to allow creation of a table of contents on specific pages
* [Admonitions](https://python-markdown.github.io/extensions/admonition/) provides support for call outs

Any markdown files you plan to use for this documentation, including the documentation markdown, can be viewed by saving the file in the `FreeEnt/server/markdown` folder, and then navigating to `/markdown_test?md_file=your_file_name`. If you leave the query string parameter (`?md_file=your_file_name`) off, you'll get this documentation file.

# Basic Markdown (this is an H1)
Since a page is supposed to only have one h1 element, and the title section is using an h1, it would be technically incorrect to include any of this style header in your markdown. See the [table of contents](#table-of-contents) section for an example of using proved classes to style headers as different header levels.

## Here's an h2

### Third time's the charm for an H3

#### H4? ff4head

##### H5 quint! quint! quint!

###### H6 is nicer than C5

Here is an example of **Bold Text**. Here is some _italicized text_.

Some of this `text is in a code block`

test
{: .code }

### `Omode:external` {: class="h6 monospace" } 

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

### Definiton Lists 
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

## Table of Contents
The table of contents extension lets you add `\[toc\]` to a markdown file (most usefully at the top) and will automatically create a table of contents for you. This has a neat side effect of automatically adding ids to your headers that are included in the table of contents, which can make it easy to link to that header from the /make page, if you'd want. By default, this is your header's text converted to kebab case (so "My Header" becomes "my-header"). If you have multiple headers with the same exact text, it numbers them as described in the [documentation](https://python-markdown.github.io/extensions/toc/#syntax).

To help support some different style options and filing out the depth of the table of contents as flexibly as possible, all of the header styles on the element also have a corresponding class. That way you can have a headers with different visual impact but the same semantic structure.

For an example:

### This is a normal h3
### And this is H3 styled as an H2, 2H2Furious {: .h2 }
which you can see is the same styling as the header for the next section.

## Attribute Lists
Using the Attribute Lists extension isn't something I've made an example for in this first pass at documentation, but they allow for some significant customization by allowing you to add a list of html attributes (like an id, or css classes, or any key/value pair you want as an attribute on your element).

One example of using them is to change how a header reads in the Table of Contents if you add one to your page, like this:
### Example h3 { #example-change-id .code data-toc-label='Changed For Content' }
For this example, I added `{ #example-change-id data-toc-label='Changed For Content' }` on the same line as the header. If you add an id (`#example-change-id`) that overrides the default behavior of using a kebab-cased version of your header's text as the element id in the html. The `data-toc-label='Changed For Content'` is how you set the text in the table of contents to be different than the header listed.

You can either include or leave off a colon after the left curly brace. So both `{ #example-change-id data-toc-label='Changed For Content' }` and `{: #example-change-id data-toc-label='Changed For Content' }` are valid. Specifically for how things interact in the TOC extension that can build a table of contents for you, adding classes won't get pulled into toc.

To end where this documentation began, go to [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/) for specifics.