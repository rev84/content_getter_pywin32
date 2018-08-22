# content_getter_pywin32

python2系。
ローカルWebサーバとして動作し、Web上のコンテンツを取得してJSONで返すスクリプト。  
Windowsサービスとして常駐する。

pywin32を使う。
https://sourceforge.net/projects/pywin32/

# インストール方法

- （pywin32をインストールしてない場合）pywin32をインストール
- コマンドプロンプトを管理者権限で起動
- 移動（例：`cd /d F:\Dropbox\git\content_getter_pywin32`）
- （既に起動している場合）`python content_getter.py stop`およびタスクマネージャーから`pythonservice.exe`をkill
- `python content_getter.py install`
- `python content_getter.py start`
- コントロールパネルのサービスの管理から、Web Content Getterを自動起動にするなど


## License
MIT
