import io
import streamlit as st

def find_end_of_first_csv_record(file_handle):
    """
    Find the byte position immediately after the first complete CSV record.

    Handles:
    - Quoted fields
    - Escaped double quotes
    - Embedded line breaks inside quoted fields
    - CRLF and LF line endings
    """
    inside_quotes = False

    while True:
        byte = file_handle.read(1)

        if not byte:
            return file_handle.tell()

        if byte == b'"':
            if inside_quotes:
                next_byte = file_handle.read(1)

                if next_byte == b'"':
                    # Escaped double quote
                    continue

                inside_quotes = False

                if next_byte:
                    file_handle.seek(-1, 1)
            else:
                inside_quotes = True

        elif byte == b"\n" and not inside_quotes:
            return file_handle.tell()


def file_ends_with_newline(file_data):
    """Return True if file data ends with a newline."""
    if not file_data:
        return True
    return file_data[-1:] in (b"\n", b"\r")


def combine_csv_files(file_data_list):
    """
    Combine multiple CSV files in the supplied order.

    The first file's header is retained. Headers in subsequent files
    are skipped. File content is copied as raw bytes to avoid changing
    quoting, Unicode characters, line endings, or multiline fields.
    """
    output_data = b""

    for index, file_data in enumerate(file_data_list):
        if index > 0:
            # Skip the header in every file after the first one.
            file_handle = io.BytesIO(file_data)
            end_of_header = find_end_of_first_csv_record(file_handle)
            file_data = file_data[end_of_header:]

            # Prevent records from joining onto the same line.
            if output_data and not file_ends_with_newline(output_data):
                output_data += b"\n"

        output_data += file_data

    return output_data


def main():
    st.set_page_config(page_title="CSV Merger", layout="centered")
    st.title("CSV Merger")
    st.markdown("Combine multiple CSV files while preserving the header from the first file.")

    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type="csv",
        accept_multiple_files=True,
        help="Select 2 or more CSV files. The first file's header will be retained."
    )

    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) selected")

        if len(uploaded_files) < 2:
            st.warning("⚠️ Please upload at least 2 CSV files to combine.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                output_filename = st.text_input(
                    "Output filename",
                    value="Output.csv",
                    help="Enter the desired output filename"
                )
            with col2:
                st.write("")
                st.write("")
                combine_button = st.button("Merge CSVs", type="primary")

            if combine_button:
                try:
                    # Read all files as bytes
                    file_data_list = [file.read() for file in uploaded_files]

                    # Combine files
                    combined_data = combine_csv_files(file_data_list)

                    # Ensure filename ends with .csv
                    if not output_filename.lower().endswith(".csv"):
                        final_filename = output_filename + ".csv"
                    else:
                        final_filename = output_filename

                    # Provide download button
                    st.success("✅ Files merged successfully!")
                    st.download_button(
                        label="Download output CSV",
                        data=combined_data,
                        file_name=final_filename,
                        mime="text/csv",
                    )

                except (OSError, ValueError) as error:
                    st.error(f"❌ Error: {error}")


if __name__ == "__main__":
    main()