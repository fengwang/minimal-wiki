## Minimal Wiki

This wiki is designed to work with self-hosted knowledge management, i.e., all pages are located in a local folder `wiki`, and this fold is synchronised with a cloud-driver across different machines.

Usage:

```bash
git clone https://github.com/fengwang/minimal-wiki.git
cd minimal-wiki
virtualenv .
source ./bin/activate
pip3 install -r ./requirements.txt
python3 ./wiki.py&
```


### Features:

#### Integration of local images

Links to local images are possible.
It is highly recommanded to place your images in folder `./wiki/images/`.
To refer a local image `./wiki/images/cat.jpg`, the desired Markdown code is

```
![](./images/cat.jpg)
```

<br>

#### Code Support

The code are highlighted with [prismjs](https://prismjs.com/), all the supported languages are list [here](https://prismjs.com/#languages-list).

To highlight a C++ code snipnet, the Markdown code is

    ```language-cpp
    #include <iostream>
    int main()
    {
       std::cout << "Hello World!\n";
       return 0;
    }
    ```

#### Equation

[MathJax](https://www.mathjax.org/) is employed to generate equations, example:

```language-none
\\[x = \\frac{-b \\pm \\sqrt{b^2-4ac} }{2a}\\]
```

And the inline equation  is generated via

```language-none
\\(x = \\frac{-b \\pm \\sqrt{b^2-4ac} }{2a}\\).
```


