import textwrap


def log(text: str) -> None:
    if "\n" in text:
        s = text.split("\n")
        for i in s:
            print(wrapper.fill(i))
    else:
        print(wrapper.fill(text))


def logo(text: str) -> None:
    print(wrapper.fill("[OK] " + text))


def logw(text: str) -> None:
    print(wrapper.fill("[WARNING] " + text))


def loge(text: str) -> None:
    if "\n" in text:
        s = text.split("\n")
        print(wrapper.fill("[ERROR]"))
        for i in s:
            print(wrapper.fill(i))
    else:
        print(wrapper.fill("[ERROR]" + text))


def indent() -> None:
    wrapper.initial_indent = 3 * " " + wrapper.initial_indent
    wrapper.subsequent_indent = 3 * " " + wrapper.subsequent_indent


def unindent() -> None:
    wrapper.initial_indent = wrapper.initial_indent[3:]
    wrapper.subsequent_indent = wrapper.subsequent_indent[3:]


def indent_reset() -> None:
    wrapper.initial_indent = "* "
    wrapper.subsequent_indent = "   "


wrapper = textwrap.TextWrapper()
wrapper.width = 120
indent_reset()
