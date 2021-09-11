# -*- coding: utf-8 -*-

#  isida bot support module

#   Copyright (C) 2012 diSabler <dsy@dsy.name>
#   Copyright © 2009-2012 Ancestors Soft

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from fatalapi import *
import sijs as json
from . import chardet
import html.entities
import calendar
import datetime

pasteurl = '<some_paste_site>'
data_folder = 'plugins/isidabot/data/%s'
date_file = 'plugins/isidabot/data/date.txt'
lcdir = 'plugins/isidabot/locales/%s'
plugdir = 'plugins/isidabot/plugins'
msg_limit = 2000
selfjid = ''

isiLocale = fLocale('\t')

isidadb = 'plugins/isidabot/plugins/isida.db'

ftiacc = {0: 0, 1: 0, 2: 0, 3: 10, 4: 11, 5: 15, 6: 16, 7: 20, 8: 30, 9: 100}
isiacc = {0: 2, 10: 3, 11: 4, 15: 5, 16: 6, 20: 7, 30: 8, 100: 9}

executes = []
msgs_hnd = []
message_act_control = []
message_control = []

def L(text):
    lcstr = isiLocale.getString(text)
    
    if not lcstr:
        lcstr = l(text)

    return lcstr

lmass = (('\n','<br>'),('\n','<br />'),('\n','<br/>'),('\n','\n\r'),('','<![CDATA['),('',']]>'),
        ('','&shy;'),('','&ensp;'),('','&emsp;'),('','&thinsp;'),('','&zwnj;'),('','&zwj;'))

rmass = (('&','&amp;'),('\"','&quot;'),('\'','&apos;'),('~','&tilde;'),(' ','&nbsp;'),
        ('<','&lt;'),('>','&gt;'),('¡','&iexcl;'),('¢','&cent;'),('£','&pound;'),
        ('¤','&curren;'),('¥','&yen;'),('¦','&brvbar;'),('§','&sect;'),('¨','&uml;'),('©','&copy;'),('ª','&ordf;'),
        ('«','&laquo;'),('¬','&not;'),('®','&reg;'),('¯','&macr;'),('°','&deg;'),('±','&plusmn;'),
        ('²','&sup2;'),('³','&sup3;'),('´','&acute;'),('µ','&micro;'),('¶','&para;'),('·','&middot;'),('¸','&cedil;'),
        ('¹','&sup1;'),('º','&ordm;'),('»','&raquo;'),('¼','&frac14;'),('½','&frac12;'),('¾','&frac34;'),('¿','&iquest;'),
        ('×','&times;'),('÷','&divide;'),('À','&Agrave;'),('Á','&Aacute;'),('Â','&Acirc;'),('Ã','&Atilde;'),('Ä','&Auml;'),
        ('Å','&Aring;'),('Æ','&AElig;'),('Ç','&Ccedil;'),('È','&Egrave;'),('É','&Eacute;'),('Ê','&Ecirc;'),('Ë','&Euml;'),
        ('Ì','&Igrave;'),('Í','&Iacute;'),('Î','&Icirc;'),('Ï','&Iuml;'),('Ð','&ETH;'),('Ñ','&Ntilde;'),('Ò','&Ograve;'),
        ('Ó','&Oacute;'),('Ô','&Ocirc;'),('Õ','&Otilde;'),('Ö','&Ouml;'),('Ø','&Oslash;'),('Ù','&Ugrave;'),('Ú','&Uacute;'),
        ('Û','&Ucirc;'),('Ü','&Uuml;'),('Ý','&Yacute;'),('Þ','&THORN;'),('ß','&szlig;'),('à','&agrave;'),('á','&aacute;'),
        ('â','&acirc;'),('ã','&atilde;'),('ä','&auml;'),('å','&aring;'),('æ','&aelig;'),('ç','&ccedil;'),('è','&egrave;'),
        ('é','&eacute;'),('ê','&ecirc;'),('ë','&euml;'),('ì','&igrave;'),('í','&iacute;'),('î','&icirc;'),('ï','&iuml;'),
        ('ð','&eth;'),('ñ','&ntilde;'),('ò','&ograve;'),('ó','&oacute;'),('ô','&ocirc;'),('õ','&otilde;'),('ö','&ouml;'),
        ('ø','&oslash;'),('ù','&ugrave;'),('ú','&uacute;'),('û','&ucirc;'),('ü','&uuml;'),('ý','&yacute;'),('þ','&thorn;'),
        ('ÿ','&yuml;'),('∀','&forall;'),('∂','&part;'),('∃','&exists;'),('∅','&empty;'),('∇','&nabla;'),('∈','&isin;'),
        ('∉','&notin;'),('∋','&ni;'),('∏','&prod;'),('∑','&sum;'),('−','&minus;'),('∗','&lowast;'),('√','&radic;'),
        ('∝','&prop;'),('∞','&infin;'),('∠','&ang;'),('∧','&and;'),('∨','&or;'),('∩','&cap;'),('∪','&cup;'),
        ('∫','&int;'),('∴','&there4;'),('∼','&sim;'),('≅','&cong;'),('≈','&asymp;'),('≠','&ne;'),('≡','&equiv;'),
        ('≤','&le;'),('≥','&ge;'),('⊂','&sub;'),('⊃','&sup;'),('⊄','&nsub;'),('⊆','&sube;'),('⊇','&supe;'),
        ('⊕','&oplus;'),('⊗','&otimes;'),('⊥','&perp;'),('⋅','&sdot;'),('Α','&Alpha;'),('Β','&Beta;'),('Γ','&Gamma;'),
        ('Δ','&Delta;'),('Ε','&Epsilon;'),('Ζ','&Zeta;'),('Η','&Eta;'),('Θ','&Theta;'),('Ι','&Iota;'),('Κ','&Kappa;'),
        ('Λ','&Lambda;'),('Μ','&Mu;'),('Ν','&Nu;'),('Ξ','&Xi;'),('Ο','&Omicron;'),('Π','&Pi;'),('Ρ','&Rho;'),
        ('Σ','&Sigma;'),('Τ','&Tau;'),('Υ','&Upsilon;'),('Φ','&Phi;'),('Χ','&Chi;'),('Ψ','&Psi;'),('Ω','&Omega;'),
        ('α','&alpha;'),('β','&beta;'),('γ','&gamma;'),('δ','&delta;'),('ε','&epsilon;'),('ζ','&zeta;'),('η','&eta;'),
        ('θ','&theta;'),('ι','&iota;'),('κ','&kappa;'),('λ','&lambda;'),('μ','&mu;'),('ν','&nu;'),('ξ','&xi;'),
        ('ο','&omicron;'),('π','&pi;'),('ρ','&rho;'),('ς','&sigmaf;'),('σ','&sigma;'),('τ','&tau;'),('υ','&upsilon;'),
        ('φ','&phi;'),('χ','&chi;'),('ψ','&psi;'),('ω','&omega;'),('ϑ','&thetasym;'),('ϒ','&upsih;'),('ϖ','&piv;'),
        ('Œ','&OElig;'),('œ','&oelig;'),('Š','&Scaron;'),('š','&scaron;'),('Ÿ','&Yuml;'),('ƒ','&fnof;'),('ˆ','&circ;'),
        ('','&lrm;'),('','&rlm;'),('–','&ndash;'),('—','&mdash;'),('‘','&lsquo;'),('’','&rsquo;'),('‚','&sbquo;'),
        ('“','&ldquo;'),('”','&rdquo;'),('„','&bdquo;'),('†','&dagger;'),('‡','&Dagger;'),('•','&bull;'),('…','&hellip;'),
        ('‰','&permil;'),('′','&prime;'),('″','&Prime;'),('‹','&lsaquo;'),('›','&rsaquo;'),('‾','&oline;'),('€','&euro;'),
        ('™','&trade;'),('←','&larr;'),('↑','&uarr;'),('→','&rarr;'),('↓','&darr;'),('↔','&harr;'),('↵','&crarr;'),
        ('⌈','&lceil;'),('⌉','&rceil;'),('⌊','&lfloor;'),('⌋','&rfloor'),('◊','&loz;'),('♠','&spades;'),('♣','&clubs;'),
        ('♥','&hearts;'),('♦','&diams;'))

config_prefs = {'url_title': [L('Url title is %s'), L('Automatic show title of urls in conference'), [True,False], False],
                'content_length': [L('Content length %s'), L('Automatic show lenght of content in conference'), [True,False], False],
                'censor': [L('Censor is %s'), L('Censor'), [True,False], False],
                #'censor_message': [L('Censor message is %s'), L('Censor message'), None, censor_text],
                'censor_warning': [L('Censor warning is %s'), L('Warning for moderators and higher') ,[True,False], False],
                'censor_action_member': [L('Censor action for member is %s'), L('Censor action for member'), ['off','visitor','kick','ban'], 'off'],
                'censor_action_non_member': [L('Censor action for non member is %s'), L('Censor action for non member'), ['off','visitor','kick','ban'], 'off'],
                'censor_custom': [L('Custom censor is %s'), L('Custom censor'), [True,False], False],
                'censor_custom_rules': [L('Custom rules for censor is %s'), L('Custom rules for censor'), None, '\n'],
                'parse_define': [L('Parse define is %s'), L('Automatic parse definition via google'), ['off','full','partial'], 'off'],
                'clear_answer':[L('Clear notification by %s'),L('Clear notification by presence or message'), ['presence','message'],'presence'],
                'autoturn': [L('Autoturn layout of text is %s'), L('Turn text from one layout to another.'), [True,False], False],
                'make_stanza_jid_count':[L('Jid\'s per stanza for affiliations in backup is %s'),L('Count of jid\'s per stanza for affiliations change in backup'),None,'100'],
                'acl_multiaction': [L('ACL multiaction is %s'), L('Execute more than one action per pass in ACL.'), [True,False], False],
                'paste_xhtml_images': [L('Paste xhtml images %s'), L('Detect and paste xhtml images in messages'), [True,False], True],

                # MUC-Filter messages

                'muc_filter': [L('Muc filter is %s'), L('Message filter for participants'), [True,False], False],
                'muc_filter_newbie': [L('Mute newbie %s'), L('Mute all messages from newbie'), [True,False], False],
                'muc_filter_newbie_repeat': [L('Count of messages for newbie %s'), L('Count of messages for newbie for action'), None, '3'],
                'muc_filter_newbie_repeat_action': [L('Action for messages overflow for newbie %s'), L('Action for messages overflow for newbie'), ['off','kick','ban'], 'off'],
                'muc_filter_newbie_time': [L('Mute newbie time %s'), L('Time of mute all messages from newbie'), None, '60'],
                'muc_filter_adblock': [L('Adblock muc filter is %s'), L('Adblock filter'), ['off','visitor','kick','ban','replace','mute'], 'off'],
                'muc_filter_repeat': [L('Repeat muc filter is %s'), L('Repeat same messages filter'), ['off','visitor','kick','ban','mute'], 'off'],
                'muc_filter_match': [L('Match muc filter is %s'), L('Repeat text in message filter'), ['off','visitor','kick','ban','mute'], 'off'],
                'muc_filter_large': [L('Large muc filter is %s'), L('Large message filter'), ['off','visitor','kick','ban','paste','truncate','mute'], 'off'],
                'muc_filter_censor': [L('Censor muc filter is %s'), L('Censor filter'), ['off','visitor','kick','ban','replace','mute'], 'off'],
                'muc_filter_adblock_raw': [L('Raw adblock muc filter is %s'), L('Raw adblock filter'), ['off','visitor','kick','ban','mute'], 'off'],
                'muc_filter_censor_raw': [L('Raw censor muc filter is %s'), L('Raw censor filter'), ['off','visitor','kick','ban','mute'], 'off'],
                'muc_filter_raw_percent': [L('Persent of short words for raw actions is %s'), L('Persent of short words for raw actions'), None, '40'],
                'muc_filter_reduce_spaces_msg': [L('Reduce spaces in message %s'), L('Reduce duplicates of spaces in message'), [True,False], False],

                # MUC-Filter presence

                'muc_filter_history': [L('Block joins without history %s'), L('Block joins without history'), [True,False], True],
                'muc_filter_adblock_prs': [L('Adblock muc filter for presence is %s'), L('Adblock filter for presence'), ['off','kick','ban','replace','mute'], 'off'],
                'muc_filter_rejoin': [L('Repeat join muc filter is %s'), L('Repeat join muc filter'), [True,False], False],
                'muc_filter_whitelist': [L('Whitelist is %s'), L('Whitelist via muc filter'), [True,False], False],
                'muc_filter_blacklist': [L('Blacklist is %s'), L('Blacklist via muc filter'), [True,False], False],
                'muc_filter_blacklist_rules_jid': [L('Blacklist rules for jid\'s %s'), L('Jid\'s rules for blacklist via muc filter.'), None, ''],
                'muc_filter_blacklist_rules_nick': [L('Blacklist rules for nick\'s %s'), L('Nick\'s rules for blacklist via muc filter.'), None, ''],
                'muc_filter_newline': [L('New line in presence muc filter is %s'), L('New line muc filter'), ['off','kick','ban','mute','replace'], 'off'],
                'muc_filter_newline_count': [L('New line count in presence muc filter is %s'), L('Count of new line muc filter'), None, '2'],
                'muc_filter_newline_msg': [L('New line in message muc filter is %s'), L('New line muc filter'), ['off','kick','ban','mute','replace'], 'off'],
                'muc_filter_newline_msg_count': [L('New line count in message muc filter is %s'), L('Count of new line muc filter'), None, '2'],
                'muc_filter_repeat_prs': [L('Repeat presence muc filter is %s'), L('Repeat presence muc filter'), ['off','kick','ban','mute'], 'off'],
                'muc_filter_large_nick': [L('Large nick muc filter is %s'), L('Large nick muc filter'), ['off','visitor','kick','ban','truncate','mute'], 'off'],
                'muc_filter_large_status': [L('Large status muc filter is %s'), L('Large status muc filter'), ['off','visitor','kick','ban','truncate','mute'], 'off'],
                'muc_filter_censor_prs': [L('Censor muc filter for presence is %s'), L('Censor muc filter for presence'), ['off','kick','ban','replace','mute'], 'off'],
                'muc_filter_deny_hash': [L('Deny by hash %s'), L('Lock joins via hash'), [True,False], False],
                'muc_filter_deny_hash_list': [L('Deny hashes list %s'), L('Hashes list for lock joins'), None, ''],
                'muc_filter_hash': [L('Hash. Check activity %s'), L('Actions by hash activity'), [True,False], False],
                'muc_filter_hash_ban_by_rejoin': [L('Hash. Ban if hash activity %s'), L('Actions for ban by hash activity'), [True,False], True],
                'muc_filter_hash_ban_by_rejoin_timeout': [L('Hash. Timeout for clean hash activity %s'), L('Time period for clean hash activity'), None, '600'],
                'muc_filter_hash_ban_server_by_rejoin': [L('Hash. Ban server by hash activity %s'), L('Ban server by hash activity'), [True,False], True],
                'muc_filter_hash_ban_server_by_rejoin_exception': [L('Hash. Exception for ban servers %s'), L('Exception for ban servers'), None, ''],
                'muc_filter_hash_ban_server_by_rejoin_notify_jid': [L('Hash. Jid\'s for servers ban notify %s'), L('Jid\'s for servers ban notify'), None, ''],
                'muc_filter_hash_ban_server_by_rejoin_rejoins': [L('Hash. Count of rejoins from server for ban %s'), L('Count of rejoins from server for ban'), None, '5'],
                'muc_filter_hash_ban_server_by_rejoin_timeout': [L('Hash. Timeout of rejoins from server for ban %s'), L('Timeout of rejoins from server for ban'), None, '60'],
                'muc_filter_hash_time': [L('Hash. Time for events %s'), L('Time period for events'), None, '20'],
                'muc_filter_hash_events': [L('Hash. Events count %s'), L('Events count per time period'), None, '10'],
                'muc_filter_hash_action': [L('Hash. Action type %s'), L('Type of action'), ['whitelist','lock by hash'], 'whitelist'],
                'muc_filter_hash_action_time': [L('Hash. Time to disable action %s'), L('Time to disable action'), None, '1800'],
                'muc_filter_hash_action_current': [L('Hash. Action for already joined %s'), L('Action for already joined'), ['off','kick','ban'], 'off'],
                'muc_filter_censor_prs_raw': [L('Raw censor muc filter for presence is %s'), L('Raw censor muc filter for presence'), ['off','kick','ban','mute'], 'off'],
                'muc_filter_adblock_prs_raw': [L('Raw adblock muc filter for presence is %s'), L('Raw adblock filter for presence'), ['off','kick','ban','mute'], 'off'],
                'muc_filter_reduce_spaces_prs': [L('Reduce spaces in presence %s'), L('Reduce duplicates of spaces in presence'), [True,False], False],
                #'muc_filter_caps': [L('Limitation by caps %s'), L('Limitation to join by caps'), [True,False], False],
                'muc_filter_caps_list': [L('Type of list %s'), L('Type of list for caps'), ['off','black','white'], 'off'],
                'muc_filter_caps_white': [L('Whitelist %s'), L('Whitelist for caps'), None, '\n'],
                'muc_filter_caps_black': [L('Blacklist %s'), L('Blacklist for caps'), None, '\n'],
                #'muc_filter_caps_smart': [L('Smart lists %s'), L('Smart lists for caps'), [True,False], False],
                #'muc_filter_caps_white_smart': [L('Smart whitelist %s'), L('Smart whitelist for caps'), None, '\n'],
                #'muc_filter_caps_black_smart': [L('Smart blacklist %s'), L('Smart blacklist for caps'), None, '\n'],
                'muc_filter_validate_action': [L('Action for invalid items %s'), L('Action for invalid items'), ['off','ban','ban server'], 'ban'],
                'muc_filter_validate_nick': [L('Validate nick %s'), L('Validate nick'), [True,False], True],
                'muc_filter_validate_login': [L('Validate login %s'), L('Validate login'), [True,False], True],
                'muc_filter_validate_resource': [L('Validate resource %s'), L('Validate resource'), [True,False], True],
                'muc_filter_validate_caps_node': [L('Validate caps node %s'), L('Validate caps node'), [True,False], True],
                'muc_filter_validate_caps_version': [L('Validate caps version %s'), L('Validate caps version'), [True,False], True],
                'muc_filter_validate_count': [L('Count of invalid items %s'), L('Count of invalid items for action'), None, '4'],
                'muc_filter_validate_ban_server_exception': [L('Exception for ban servers %s'), L('Exception for ban servers'), None, ''],
                'muc_filter_validate_ban_server_notify_jid': [L('Jid\'s for servers ban notify %s'), L('Jid\'s for servers ban notify'), None, ''],

                # Bomb

                'bomb': [L('Bomb. Allow take a bomb %s'), L('Allow take a bomb in current conference'), [True,False], True],
                'bomb_fault': [L('Bomb. Allow random unexplosive bombs %s'), L('Allow some times take unexplosive bombs'), [True,False], True],
                'bomb_fault_persent': [L('Bomb. Persent of fault bombs %s'), L('Persent of fault bombs'), None, '25'],
                'bomb_random': [L('Bomb. Allow bot take a bomb to random user %s'), L('Allow bot take a bomb to random user'), [True,False], False],
                'bomb_random_active': [L('Bomb. Allow random bombs only in active room %s'), L('Allow random bombs only in active room'), [True,False], True],
                'bomb_random_active_timer': [L('Bomb. Time for detect room as unactive %s'), L('Time for detect room as unactive'), None, '1200'],
                'bomb_random_timer': [L('Bomb. Time between random bombs %s'), L('Time between random bombs'), None, '1800'],
                'bomb_random_timer_persent': [L('Bomb. Persent of mistakes for time between random bombs %s'), L('Persent of mistakes for time between random bombs'), None, '25'],
                'bomb_random_timer_skip_persent': [L('Bomb. Persent of skiped random bombs %s'), L('Persent of mistakes skiped random bombs'), None, '25'],
                'bomb_timer': [L('Bomb. Timer is %s'), L('Time to deactivate a bomb'), None, '45'],
                'bomb_wire': [L('Bomb. Wire count is %s'), L('Wire count for bomb'), None, '4'],
                'bomb_action': [L('Bomb. Action for bomb explode %s'), L('Type of action for bomb explode'), ['off','kick'], 'kick'],
                'bomb_action_level': [L('Bomb. Don\'t use action when access level lower than or equal %s'), L('Ignore bomb action depends from access level'), ['4','5','6','7','8','9'], '4'],
                'bomb_reason': [L('Bomb. Reason %s'), L('Reason for bomb explode'), None, L('KA-BO-OM!!!111')],
                'bomb_idle': [L('Bomb. Idle for unable get the bomb %s'), L('Idle for unable get the bomb'), None, '900'],

                # Karma actions

                'karma_action': [L('Karma. Actions for karma change is %s'), L('Allow change role/affiliation by karma change'), [True,False], False],
                'karma_action_reason': [L('Karma. Reason for actions by karma change is %s'), L('Reason for change role/affiliation by karma change'), None, L('by karma change!')],
                'karma_action_1ban': [L('Karma. Ban when karma is lower than %s'), L('Ban when karma is lower than defined value'), None, '-50'],
                'karma_action_2kick': [L('Karma. Kick when karma is lower than %s'), L('Kick when karma is lower than defined value'), None, '-20'],
                'karma_action_3visitor': [L('Karma. Revoke voice when karma is lower than %s'), L('Revoke voice when karma is lower than defined value'), None, '-10'],
                'karma_action_4none': [L('Karma. None affiliation when karma is lower than %s'), L('Revoke affiliation when karma is lower than defined value'), None, '-5'],
                'karma_action_5participant': [L('Karma. Participant affiliation when karma is higher than %s'), L('Give a participant affiliation when karma is higher than defined value'), None, '5'],
                'karma_action_6member': [L('Karma. Member affiliation when karma is higher than %s'), L('Give a member affiliation when karma is higher than defined value'), None, '20'],
                'karma_action_7moderator': [L('Karma. Moderator role when karma is higher than %s'), L('Give a moderator role when karma is higher than defined value'), None, '50'],
                'karma_hard': [L('Hard rule for karma is %s'), L('Not allow any symbols between nick and karma digit') ,[True,False], False],
                'karma_limit': [L('Limits for karma change is %s'), L('Limitation of karma\'s change. Depends of access level') ,[True,False], True],
                'karma_limit_size': [L('Value of limits for karma change %s'), L('Value of limitation of karma\'s change. Depends of access level') ,None, '[3,5]'],

                # Flood
                'flood': [L('Flood is %s'), L('Autoanswer'), ['off','random','smart'], 'off'],
                'autoflood': [L('Autoflood is %s'), L('Autoflood'), [True,False], False],
                'floodcount': [L('Number of message for autoflood\'s start: %s'), L('Number of message for autoflood\'s start'), None, '3'],
                'floodtime': [L('Time period for autoflood\'s start: %s'), L('Time period for autoflood\'s start'), None, '1800'],
                'autophrases': [L('Autophrases is %s'), L('Autophrases'), ['off','without highlight','all'], 'off'],
                'autophrasestime': [L('Time period for autophrases is %s'), L('Time period for autophrases'), None, '7200']

                }

owner_prefs = {'syslogs_enable': [L('Logger. Enable system logs'),'b',True],
                'status_logs_enable':[L('Logger. Enable status change logging'),'b',True],
                'aff_role_logs_enable':[L('Logger. Enable role and affiliation logging'),'b',True],
                'html_logs_enable':[L('Logger. Html logs. Otherwize in text'),'b',True],
                'html_logs_end_text':[L('Logger. Additional text for logs'),'m512',''],
                'karma_limit':[L('Karma. Minimal karma for allow krama change for participants'),'i',5],
                'karma_show_default_limit':[L('Karma. Default length of list karma top+/-'),'i',10],
                'karma_show_max_limit':[L('Karma. Maximal length of list karma top+/-'),'i',20],
                'watch_size':[L('Watcher. Frequency of requests in watcher'),'i',900],
                'user_agent':[L('Www. User-agent for web queries'),'m256','Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'],
                'size_overflow':[L('Www. Limit of page in bytes for www command'),'i',262144],
                'youtube_max_videos':[L('Youtube. Maximal links number'),'i',10],
                'youtube_default_videos':[L('Youtube. Default links number'),'i',3],
                'youtube_max_page_size':[L('Youtube. Page size limit'),'i',131072],
                'youtube_default_lang':[L('Youtube. Default language'),'t2','ru'],
                'age_default_limit':[L('Age. Default number of users for age commands'),'i',10],
                'age_max_limit':[L('Age. Maximal number of users for age commands'),'i',100],
                'anek_private_limit':[L('Anek. Anekdote size for private send'),'i',500],
                'troll_default_limit':[L('Troll. Default message number for troll command'),'i',10],
                'troll_max_limit':[L('Troll. Maximal message number for troll command'),'i',100],
                'troll_sleep_time':[L('Troll. Delay between messages for troll command'),'f',0.05],
                'backup_sleep_time':[L('Backup. Requests delay for backup command'),'f',0.1],
                'calendar_default_splitter':[L('Calendar. Default splitter for calendar'),'t10','_'],
                'clear_delay':[L('Clear. Delay between massages in clear command'),'f',1.3],
                'clear_default_count':[L('Clear. Default message number for clear command'),'i',20],
                'clear_max_count':[L('Clear. Maximal message number for clear command'),'i',100],
                'ping_digits':[L('Iq. Number after point in ping'),'i',3],
                'lfm_api':[L('LastFM. Api for lastfm plugin'),'t64','no api'],
                'lastfm_max_limit':[L('LastFM. Number of answers for lastfm plugin'),'i',10],
                'reboot_time':[L('Kernel. Restart timeout for error at bot initial (no connection, auth error)'),'i',180],
                'timeout':[L('Iq. Timeout for iq queries'),'i',600],
                'schedule_time':[L('Kernel. Schedule time'),'i',10],
                'sayto_timeout':[L('Sayto. Age of message in sayto before delete it from base with undelivered'),'i',1209600],
                'sayto_cleanup_time':[L('Sayto. Timeout for sayto base cleanup'),'i',86400],
                'scan_time':[L('Spy. Time for spy scan'),'i',1800],
                'spy_action_time':[L('Spy. Time for reaction on spy scan'),'i',86400],
                'rss_max_feed_limit':[L('Rss. Maximum rss count'),'i',10],
                'rss_min_time_limit':[L('Rss. Minimal time for rss check in minutes'),'i',10],
                'rss_get_timeout':[L('Rss. Timeout for rss request from server in seconds'),'i',15],
                'whereis_time_dec':[L('Whereis. Frequency for answer check for whereis command'),'f',0.5],
                'watcher_room_activity':[L('Watcher. Try rejoin in rooms with low activity'),'b',True],
                'watcher_self_ping':[L('Watcher. Allow self ping'),'b',True],
                'disco_max_limit':[L('Disco. Maximus andwers count for disco command'),'i',10],
                'juick_user_post_limit':[L('Juick. Number of posts'),'i',10],
                'juick_user_post_size':[L('Juick. Number of symbols in post'),'i',50],
                'juick_msg_answers_default':[L('Juick. Number of answers'),'i',10],
                'juick_user_tags_limit':[L('Juick. Number of tags'),'i',10],
                'iq_time_enable':[L('Iq. Allow answer to time request'),'b',True],
                'iq_uptime_enable':[L('Iq. Allow answer to uptime request'),'b',True],
                'iq_version_enable':[L('Iq. Allow answer to version request'),'b',True],
                'iq_disco_enable':[L('Iq. Allow answer to service discovery'),'b',True],
                'iq_ping_enable':[L('Iq. Allow answer to ping'),'b',True],
                'iq_show_rooms_disco':[L('Iq. Show bot rooms in service discovery'),'b',True],
                'paranoia_mode':[L('Kernel. Paranoic mode. Disable all execute possibles on bot'),'b',False],
                'show_loading_by_status':[L('Kernel. Bot status. Show different status for bot loading'),'b',True],
                'show_loading_by_status_show':[L('Kernel. Bot status. Status while loading'),'d','dnd',['chat','online','away','xa','dnd']],
                'show_loading_by_status_message':[L('Kernel. Bot status. Message while loading'),'t256',L('Loading...')],
                'show_loading_by_status_percent':[L('Kernel. Bot status. Show percent of loading'),'b',True],
                'show_loading_by_status_room':[L('Kernel. Bot status. Show join to room while loading'),'b',True],
                'kick_ban_notify':[L('Kernel. Notify when bot is kicked or banned'),'b',True],
                'kick_ban_notify_jid':[L('Kernel. Notify jid for bot kick or ban'),'t1024',''],
                'watch_activity_timeout':[L('Watcher. Timeout for no actions in room for rejoin'),'i',1800],
                'muc_filter_large_message_size':[L('Muc-filter. Message size for filter'),'i',512],
                'muc_filter_match_count':[L('Muc-filter. A kind words count'),'i',3],
                'muc_filter_match_warning_match':[L('Muc-filter. Number of kind parts in message'),'i',3],
                'muc_filter_match_warning_space':[L('Muc-filter. Number of empty parts in message'),'i',5],
                'muc_filter_match_view':[L('Muc-filter. Message limit'),'i',512],
                'muc_filter_match_warning_nn':[L('Muc-filter. Number of empty new lines'),'i',3],
                'muc_filter_rejoin_count':[L('Muc-filter. Number of reconnects for monitoring'),'i',3],
                'muc_filter_rejoin_timeout':[L('Muc-filter. Time for reconnect count'),'i',120],
                'muc_filter_status_count':[L('Muc-filter. Number of precences per time'),'i',3],
                'muc_filter_status_timeout':[L('Muc-filter. Time between presences'),'i',600],
                'muc_filter_large_status_size':[L('Muc-filter. Maximux status-message size'),'i',50],
                'muc_filter_large_nick_size':[L('Muc-filter. Maximum nick size'),'i',20],
                'muc_filter_repeat_count':[L('Muc-filter. Repeat count'),'i',3],
                'muc_filter_repeat_time': [L('Muc-filter. Timeout for repeat message'), 'i', 3600],
                'html_paste_enable':[L('Paste. Paste as html. Otherwize as text'),'b',True],
                'yandex_api_key':[L('City. Yandex.Map API-key'),'t128','no api'],
                'bing_api_key':[L('Bing. Translator API-key'),'t128','no api'],
                'censor_text':[L('Kernel. Text for hide censore'),'t32','[censored]'],
                'ddos_limit':[L('Kernel. Time of ignore for anti-ddos'),'l10','[1800,1800,1800,1800,1800,600,300,150,60,0]'],
                'ddos_diff':[L('Kernel. Anti-ddos time delay between messages'),'l10','[30,30,30,30,20,20,15,10,5,0]'],
                'ddos_iq_requests':[L('Kernel. Iq anti-ddos. Requests number'),'i',30],
                'ddos_iq_limit':[L('Kernel. Iq anti-ddos. Time limits for requests'),'i',10],
                'amsg_limit_size':[L('Msgtoadmin. Size limit for msgtoadmin'),'i',1024],
                'amsg_limit':[L('Msgtoadmin. Time limit for next message for msgtoadmin'),'l10','[86400,86400,86400,86400,86400,86400,43200,3600,1800,60]'],
                'karma_timeout':[L('Karma. Time for karma change from access level'),'l10','[86400,86400,86400,86400,86400,86400,43200,3600,1800,5]'],
                'karma_discret':[L('Karma. Difference between two action in karma'),'i',5],
                'karma_discret_lim_up':[L('Karma. Upper value of karma for control action'),'i',100],
                'karma_discret_lim_dn':[L('Karma. Lower value of karma for control action'),'i',-100],
                'disco_exclude':[L('Disco. Exclude from disco by regexps'),'m256e','([؀-ݭ)\n(ﭐ-ﻼ])\n(syria|arab)','disco_exclude_update()'],
                'exclude_messages':[L('Kernel. Exclude symbols from bot\'s messages'),'m256e','([؀-ۿ])\n([ݐ-ݿ])\n([ﭐ-﷿])\n([ﹰ-﻿])','message_exclude_update()'],
                '1st_april_joke':[L('Kernel. 1st April joke'),'b',True],
                'soft_update_resend_hash':[L('Kernel. Send new hash into rooms after soft update'),'b',False]
                }

def pprint(*text):
    pass

def readfile(filename):
    return read_file(filename)

def GT(item):
    try:
        gt_result = cur_execute_fetchone('select value from config_owner where option=%s;',(item,))[0]
        if gt_result in ['true','false','none']: gt_result = gt_result.capitalize()
    except:
        try: gt_result = owner_prefs[item][2]
        except: gt_result = None
    try: return eval(gt_result)
    except: return gt_result

#-----------------------------------------------------------------------------

plugins = os.listdir(plugdir)
plugins = rmv_sys_dirs(plugins)

for pl in plugins:
    plfile = 'plugins/isidabot/plugins/%s' % (pl)
    exec(compile(open(plfile, encoding='utf-8').read(), plfile, 'exec')) in globals()
    executes.extend(execute)
    msgs_hnd.extend(message_act_control)
    msgs_hnd.extend(message_control)

#-----------------------------------------------------------------------------

def get_level(cjid, cnick):
    source = ['%s/%s' % (cjid, cnick), cjid, cnick]
    access = user_level(source)
    aconv = 0
    
    if access in isiacc:
        aconv = isiacc[access]

    return [aconv]

def remove_sub_space(t): return ''.join([['?',l][l>=' ' or l in '\t\r\n'] for l in str(t)])

def reduce_spaces_all(text):
    text,t = text.strip(),''
    if len(text):
        for tmp in text:
            if tmp != ' ' or t[-1] != ' ': t += tmp
    return t

def deidna(text):
    def repl(t): return t.group().lower().decode('idna')
    return re.sub(r'(xn--[-0-9a-z_]*)',repl,text)

def enidna_raw(text):
    def repl(t): return t.group().lower().encode('idna')
    return re.sub('([а-я][-0-9а-я_]*)',repl,text)

def enidna(text):
    idn = re.findall('http[s]?://([-0-9a-zа-я._]*)',text,flags=re.S+re.U+re.I)
    if idn: text = text.replace(idn[0],idn[0].lower().encode('idna'))
    return text.encode('utf-8')

def tZ(val): return '%02d' % val

def timeadd(lt): return '%02d.%02d.%02d %02d:%02d:%02d' % (lt[2],lt[1],lt[0],lt[3],lt[4],lt[5])

def onlytimeadd(lt): return '%02d:%02d:%02d' % (lt[3],lt[4],lt[5])

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == '&#':
            try:
                if text[:3] == '&#x': return chr(int(text[3:-1], 16))
                else: return chr(int(text[2:-1]))
            except ValueError: pass
        else:
            try: text = chr(html.entities.name2codepoint[text[1:-1]])
            except KeyError: pass
        return text
    return re.sub('&#?\w+;', fixup, text)

def esc_min(ms):
    for tmp in rmass: ms = ms.replace(tmp[1],tmp[0])
    return ms

def get_subtag(body,tag):
    T = re.findall('%s=\"(.*?)\"' % tag,body,re.S)
    if T: return T[0]
    else: return ''

def get_tag(body,tag):
    T = re.findall('<%s.*?>(.*?)</%s>' % (tag,tag),body,re.S)
    if T: return T[0]
    else: return ''

def get_tag_full(body,tag):
    T = re.findall('(<%s[^>]*?>|</%s>)' % (tag,tag),body,re.S)
    if T and len(T)==1: return T[0]
    elif len(T) >= 2 and T[0][1:len(tag)+1] == T[1][-len(tag)-1:-1]:
        T1 = re.findall('(%s.*?%s)' % (re.escape(T[0]),re.escape(T[1])),body,re.S)
        if T1: return T1[0]
        else: return ''
    elif len(T): return T[0]
    else: return ''

def get_size_human(mt):
    if mt < 1024: return '%sb' % int(mt)
    for t in ['Kb','Mb','Gb']:
        mt = mt / 1024.0
        if mt < 1024: break
    return '%.2f%s' % (mt,t)

def replacer(msg):
    def repl(t): return '%s\n' % re.findall('<div.*?>(.*?)</div>',t.group(0),re.S+re.U+re.I)[0]
    msg = rss_replace(msg)
    msg = re.sub(r'(<div.*?>).*?(</div>)',repl,msg,flags=re.S+re.U+re.I)
    for tmp in [['<br/>','\n'],['<br />','\n']]: msg = msg.replace(*tmp)
    msg = rss_del_html(msg)
    msg = rss_replace(msg)
    msg = rss_del_nn(msg)
    return msg.replace('...','…')

def remove_replace_ltgt(text,item):
    T = re.findall('<.*?>', text, re.S)
    for tmp in T: text = text.replace(tmp,item,1)
    return text

def remove_ltgt(text): return remove_replace_ltgt(text,'')

def replace_ltgt(text): return remove_replace_ltgt(text,' ')

def rss_repl_del_html(ms,item):
    DS,SP,T = '<%s>','/%s',re.findall('<(.*?)>', ms, re.S)
    if len(T):
        for tmp in T:
            if (tmp[:3] == '!--' and tmp[-2:] == '--') or tmp[-1:] == '/':
                pattern = DS % tmp
                pos = ms.find(pattern)
                ms = ms[:pos] + item + ms[pos+len(pattern):]
    T = re.findall('<(.*?)>', ms, re.S)
    if len(T):
        for tmp in range(0,len(T)-1):
            pos = None
            TT = T[tmp].split(' ')[0]
            if TT and TT[0] != '/':
                try: pos = T.index(SP % TT,tmp)
                except: pass
                if pos:
                    pat1,pat2 = DS % T[tmp],DS % T[pos]
                    pos1 = ms.find(pat1)
                    pos2 = ms.find(pat2,pos1)
                    ms = ms[:pos1] + item + ms[pos1+len(pat1):pos2] + item + ms[pos2+len(pat2):]
    for tmp in ('hr','br','li','ul','img','dt','dd','p'):
        T = re.findall('<%s.*?>' % tmp, ms, re.S)
        for tmp1 in T: ms = ms.replace(tmp1,item,1)
    return ms

def rss_repl_html(ms): return rss_repl_del_html(ms,' ')

def rss_del_html(ms): return rss_repl_del_html(ms,'')

def unhtml_raw(page,mode):
    for a in range(0,page.count('<style')):
        ttag = get_tag_full(page,'style')
        page = page.replace(ttag,'')

    for a in range(0,page.count('<script')):
        ttag = get_tag_full(page,'script')
        page = page.replace(ttag,'')

    page = rss_replace(page)
    if mode: page = replace_ltgt(page)
    else: page = rss_repl_html(page)
    page = rss_replace(page)
    page = rss_del_nn(page)
    page = page.replace('\n ','')
    return page

def unhtml(page): return unhtml_raw(page,None)

def unhtml_hard(page): return unhtml_raw(page,True)

def rss_del_nn(ms):
    ms = ms.replace('\r',' ').replace('\t',' ')
    while '\n ' in ms: ms = ms.replace('\n ','\n')
    while len(ms) and (ms[0] == '\n' or ms[0] == ' '): ms = ms[1:]
    while '\n\n' in ms: ms = ms.replace('\n\n','\n')
    while '  ' in ms: ms = ms.replace('  ',' ')
    while '\n\n•' in ms: ms = ms.replace('\n\n•','\n•')
    while '• \n' in ms: ms = ms.replace('• \n','• ')
    return ms.strip()

def rss_replace(ms):
    for tmp in lmass: ms = ms.replace(tmp[1],tmp[0])
    return unescape(esc_min(ms))

def cur_execute_fetchone(*params):
    pass

def get_config(room,item):
    param = get_gch_param(room, item, '1')
    
    if param == '1':
        return True
    return False

def send_msg(mtype, mjid, mnick, mmessage):
    mtypes = {'groupchat': 'public', 'chat': 'private', 'console': 'console', 'null': 'null'}
    mtype = mtypes[mtype]

    if mnick or mtype == 'console':
        fjid = '%s/%s' % (mjid, mnick)

        source = [fjid, mjid, mnick]

        reply(mtype, source, mmessage)
    else:
        msg(mjid, mmessage)

def getName(jid):
    return get_usernode(jid)

def getServer(jid):
    return get_domain(jid) 

def getResourse(jid):
    return get_resource(jid)

def getRoom(jid):
    jid = str(jid)
    if jid == 'None': return jid
    if '@' in jid: return '%s@%s' % (getName(jid),getServer(jid))
    else: return getServer(jid)

def smart_encode(text,enc):
    tx,splitter = '','|'
    while splitter in text: splitter += '|'
    ttext = text.replace('</','<%s/' % splitter).split(splitter)
    for tmp in ttext:
        try: tx += str(tmp,enc)
        except: pass
    return tx

def html_encode(body):
    encidx = re.findall('encoding=["\'&]*(.*?)["\'& ]{1}',body[:1024])
    if encidx: enc = encidx[0]
    else:
        encidx = re.findall('charset=["\'&]*(.*?)["\'& ]{1}',body[:1024])
        if encidx: enc = encidx[0]
        else: enc = chardet.detect(body)['encoding']
    if body == None: body = ''
    if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
    if enc == 'ISO-8859-2':
        tx,splitter = '','|'
        while splitter in body: splitter += '|'
        tbody = body.replace('</','<'+splitter+'/').split(splitter)
        cntr = 0
        for tmp in tbody:
            try:
                enc = chardet.detect(tmp)['encoding']
                if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
                tx += str(tmp,enc)
            except:
                ttext = ''
                for tmp2 in tmp:
                    if (tmp2<='~'): ttext+=tmp2
                    else: ttext+='?'
                tx += ttext
            cntr += 1
        return tx
    else:
        try: return smart_encode(body,enc)
        except: return L('Encoding error!')

def get_opener(page_name, parameters=None):
    socket.setdefaulttimeout(GT('rss_get_timeout'))
    
    try:
        proxy_support = urllib.request.ProxyHandler({'http' : 'http://%(user)s:%(password)s@%(host)s:%(port)d' % http_proxy})
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
    except: 
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    
    opener.addheaders = [('User-agent', GT('user_agent'))]
    
    if parameters: 
        page_name += urllib.parse.urlencode(parameters)
    
    try: 
        data, result = opener.open(page_name), True
    except Exception as SM:
        try: 
            SM = str(SM)
        except: 
            SM = str(SM)
        
        data, result = L('Error! %s') % SM.replace('>','').replace('<','').capitalize(), False
    
    return data, result

def load_page(page_name, parameters=None):
    data, result = get_opener(page_name, parameters)

    if result:
        return data.read(GT('size_overflow'))
    else: 
        return data

