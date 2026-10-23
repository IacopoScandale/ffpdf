from pathlib import Path

from ffpdf.data.strings import SUB_FORMAT
from ffpdf.data.utils import add_one_to_counter, expand_input_paths, text_muted


def print_content_line(filename: str = "", new_filename: str = "") -> None:
    arrow_filename: str = "——>" if filename and new_filename else ""
    print(f"{filename:<40}{arrow_filename:^5}{new_filename:<40}")


def comm_format(
    files: list[Path],
    prefix: str | None = None,
    suffix: str | None = None,
    replace_files: bool | None = None,
) -> None:
    files = expand_input_paths(files)
    arrow: str = "->"

    # print header
    if files:
        print()
        print_content_line("Filename", "New Filename")
        print("—" * 80)  # em dash line separator

    # print content
    total_files: int = 0
    for file in files:
        if file.is_dir():
            continue

        new_file: Path = file.with_name(file.name)

        # TODO preset format (old code with lowercase letters and no spaces)

        # prefix
        if prefix:
            # arrow
            if arrow in prefix:
                old_prefix, new_prefix, *_ = prefix.split(arrow)
                # case input prefix is "->"
                if (not old_prefix) and (not new_prefix):
                    print_content_line(filename=text_muted(f"'{file.name}'"))
                    continue
                if new_file.stem.startswith(old_prefix):
                    new_stem: str = new_file.stem.replace(old_prefix, new_prefix, 1)
                    if not new_stem:
                        print_content_line(filename=text_muted(f"'{file.name}'"))
                        continue
                    new_file = new_file.with_stem(new_stem)

            # no arrow
            elif not file.stem.startswith(prefix):
                new_file = new_file.with_stem(f"{prefix}{new_file.stem}")

        # suffix
        if suffix:
            # arrow
            if arrow in suffix:
                old_suffix, new_suffix, *_ = suffix.split(arrow)
                # case input suffix is "->"
                if (not old_suffix) and (not new_suffix):
                    print_content_line(filename=text_muted(f"'{file.name}'"))
                    continue
                if new_file.stem.endswith(old_suffix):
                    new_stem: str = new_file.stem[::-1].replace(
                        old_suffix[::-1], new_suffix[::-1], 1
                    )[::-1]
                    if not new_stem:
                        print_content_line(filename=text_muted(f"'{file.name}'"))
                        continue
                    new_file = new_file.with_stem(new_stem)

            # no arrow
            elif not file.stem.endswith(suffix):
                new_file = new_file.with_stem(f"{new_file.stem}{suffix}")

        # if nothing changed or I cannot overwrite if existing
        if (new_file == file) or (new_file.exists() and not replace_files):
            print_content_line(filename=text_muted(file.name))
        else:
            try:
                file.replace(new_file)
                total_files += 1
                print_content_line(
                    filename=f"'{file.name}'",
                    new_filename=f"'{new_file.name}'",
                )
            except OSError as e:
                print(f"{new_file.name = }")
                print(repr(e))
                print_content_line(filename=text_muted(f"'{file.name}'"))

    # print footer
    if total_files > 1:
        print("—" * 80)  # em dash line separator
        print_content_line(new_filename=f"'{total_files} files renamed'")

    # +1 to usage counter
    add_one_to_counter(SUB_FORMAT)
