#  Copyright © 2022 Kalynovsky Valentin. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import enum


class SMTPHost(enum.Enum):
    """It's an enumeration of the SMTP hosts"""
    gmail = 'smtp.gmail.com'
    mail = 'smtp.mail.ru'
    freemail = 'freemail.ukr.net'


class SMTPPort(enum.Enum):
    """It's an enumeration of the SMTP ports"""
    gmail = 465
    mail = 465
    freemail = 993
