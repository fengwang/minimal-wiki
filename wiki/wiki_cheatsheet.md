## Wiki Cheatsheet

-------------------------------------------

This wiki generally supports [Mardown](https://en.wikipedia.org/wiki/Markdown) grammar, a cheatsheet is available at [Mardown-Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

Cross-links are encouraged.
For each page, there is a corresponding unique link, which can be found in the browser address bar.
To create a link to a specified page, use `[TEXT](./unique_url)`.
For example, a link to [this page](./wiki_cheatsheet) can be `[cheatsheet](./wiki_cheatsheet)`.

Features of this wik:

+ [Integration of local images](#images)
+ [Code highlight](#code)
+ [Equation](#equation)


<br>

<a name="images"/>

### Integration of local images

Links to local images are possible.
It is highly recommanded to place your images in folder `./wiki/images/`.
To refer a local image `./wiki/images/cat.jpg`, the desired Markdown code is

```language-markup
![](./images/cat.jpg)
```

This will generate an image like this:

![](./images/cat.jpg)

<br>

<a name="code"/>
### Code Support

The code are highlighted with [prismjs](https://prismjs.com/), all the supported languages are list [here](https://prismjs.com/#languages-list).

To highlight a C++ code snipnet, the Markdown code is

```language-markup
    ```language-cpp
    #include <iostream>
    int main()
    {
       std::cout << "Hello World!\n";
       return 0;
    }
    ```
```

This will result in
```language-cpp
#include <iostream>
int main()
{
    std::cout << "Hello World!\n";
    return 0;
}
```


<br>

<a name="equation"/>
### Equation

[MathJax](https://www.mathjax.org/) is employed to generate equations, example:

```language-none
\\[x = \\frac{-b \\pm \\sqrt{b^2-4ac} }{2a}\\]
```

results in

\\[x = \\frac{-b \\pm \\sqrt{b^2-4ac} }{2a}\\]

And the inline equation  \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) is generated from

```language-none
\\(x = \\frac{-b \\pm \\sqrt{b^2-4ac} }{2a}\\)
```




