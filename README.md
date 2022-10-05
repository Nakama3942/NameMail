# NameMail
The program is a solution to the task from the first laboratory on the subject "Network Information Technologies".

## Overview
This program is a mail client. Its main functionality:
- Reading mail (uses IMAP4);
- Sending mail (uses SMTP);
- Ability to send letters anonymously (if the mail host supports it);
- Possibility of mass mailing of letters;
- All background information and documentation is described in script files;
- And a lot of other important little things.

## LICENSE
The full text of the license can be found at the following [link](https://github.com/Nakama3942/NameMail/blob/main/LICENSE).

> Copyright © 2022 Kalynovsky Valentin. All rights reserved.
> 
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
> 
>     http://www.apache.org/licenses/LICENSE-2.0
> 
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.

## Usage
To start the program, just run *run.sh*.

But it is also possible to run the program through the console:
```shell
python main.py
```
Якщо програма видає помилку відсутності модулів при запуску, встановіть Qt:
If the program gives a missing modules error at startup, install Qt:
```shell
pip install PyQt6
# or
pip install pyqt6
```

## Authors
<table align="center" style="border-width: 10; border-style: ridge">
	<tr>
		<td align="center"><a href="https://github.com/Nakama3942"><img src="https://avatars.githubusercontent.com/u/73797846?s=400&u=a9b7688ac521d739825d7003a5bd599aab74cb76&v=4" width="150px;" alt=""/><br /><sub><b>Kalynovsky Valentin</b></sub></a><sub><br />"Ideological inspirer and Author"</sub></td>
		<!--<td></td>-->
	</tr>
<!--
	<tr>
		<td></td>
		<td></td>
	</tr>
-->
</table>