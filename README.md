# fumi-python-libraries

研究に使用するpythonのコードをまとめたリポジトリです。

Pythonパッケージ管理ツールryeを使っています。

## 事前整備

ryeがない場合はまずrye使えるようにしなければいけません。

Macの場合は`brew install rye`で入る。

Linuxの場合は以下のようにしてインストールしてパスを通します。

```bash
curl -sSf https://rye-up.com/get | bash
```

色々聞かれると思いますが、`y`を連打しておけばOKです。

Shellを再度起動した時にパスを通し直す必要がないように`.bashrc`にパスを追加しておきます。

```bash
echo 'source "$HOME/.rye/env"' >> ~/.bashrc
exec bash
rye --version
```

これでryeのバージョンが表示されればOKです。

## 環境整備

さてようやく`git clone`でローカルにクローンしてくる。

```bash
git clone https://github.com/FumiHubCNS/fumi-python-libraries.git
```

そのあと必要なライブラリーをとってくる。

```bash
cd fumi-python-libraries
rye sync
```

以上で完了です。以下のようなコマンドでJupyterLab Serverを立ち上げることができます。

```bash
rye run jupyter lab
```

