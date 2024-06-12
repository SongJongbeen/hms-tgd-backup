import csv
import pandas as pd

# html_path = f"{self.backup_folder}/html-{content_link.split('/')[-1]}.html"
tgd_csv = "tgd-crawler/tgd.csv"
sample_html_path = "tgd-crawler/posts/sample.html"


def make_post_html():
    with open(tgd_csv, "r", encoding="utf8") as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            category = row[2]
            title = row[3]
            link = row[4].split("/")[-1]
            author = row[5]
            date = row[6]

            content_html_path = f"tgd-crawler/backup/html-{link}.html"
            html_path = f"tgd-crawler/posts/{link}.html"

            with open(content_html_path, "r", encoding="utf8") as file:
                content_html = file.read()

            with open(sample_html_path, "r", encoding="utf8") as file:
                sample_html = file.read()

            new_html = sample_html.replace("카 테 고 리", category)
            new_html = new_html.replace("글 제 목", title)
            new_html = new_html.replace("작 성 자", author)
            new_html = new_html.replace("작 성 일", date)
            new_html = new_html.replace("콘 텐 츠", content_html)

            with open(html_path, "w", encoding="utf8") as file:
                file.write(new_html)
                print(f"Created {html_path}")

    print("Done")

def make_index_html():
    # CSV 파일을 읽기
    csv_file = tgd_csv  # CSV 파일의 경로
    data = pd.read_csv(csv_file)

    # 필요한 열만 추출
    data = data[['카테고리', '제목', '작성자', '작성일', 'id']]

    # HTML 파일 생성
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Index</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Index Page</h1>
        <table>
            <tr>
                <th>카테고리</th>
                <th>제목</th>
                <th>작성자</th>
                <th>작성일</th>
            </tr>
    """

    # 데이터 프레임을 HTML 테이블 형식으로 변환
    for index, row in data.iterrows():
        html_content += f"""
            <tr>
                <td>{row['카테고리']}</td>
                <td><a href="posts/{row['id'].split("/")[-1]}.html">{row['제목']}</a></td>
                <td>{row['작성자']}</td>
                <td>{row['작성일']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # index.html 파일로 저장
    with open('tgd-crawler/index.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print("index.html 파일이 성공적으로 생성되었습니다.")

make_post_html()
make_index_html()
