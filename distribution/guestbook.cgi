#! /usr/local/bin/perl -w


#################################################################################
#										#
#  										#
#   Guestbook v.0.4							       	#
#   Copyright (C) 2003-2004 - Steven Schubiger <steven@accognoscere.org>	#
#   Last changes: 12th November 2004						#
#										#
#   This program is free software; you can redistribute it and/or modify	#
#   it under the terms of the GNU General Public License as published by	#
#   the Free Software Foundation; either version 2 of the License, or		#
#   (at your option) any later version.						#
#										#
#   This program is distributed in the hope that it will be useful,		#
#   but WITHOUT ANY WARRANTY; without even the implied warranty of		#
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		#
#   GNU General Public License for more details.				#
#										#
#   You should have received a copy of the GNU General Public License		#
#   along with this program; if not, write to the Free Software			#
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA	#
#										#
#										#
#################################################################################




##########
# SECTION: CGI-Environment & global calls
#########################################

require 'guestbook.cfg';

use CGI;
use CGI::Carp ('fatalsToBrowser');
use integer;



my $query = new CGI;

$submit{'general'}{'mode'}{'action'} = $query->param ('action');

$submit{'general'}{'guestbook_entry'}{'start_id'} = $query->param ('guestbook_entry_start_id');
$submit{'general'}{'guestbook_entry'}{'id'} = $query->param ('guestbook_entry_id');

$submit{'general'}{'mode'}{'admin_interface'} = $query->param ('admin_interface_mode');
$submit{'admin'}{'security'}{'sid'} = $query->param ('sid');




unless ($submit{'general'}{'mode'}{'action'}) { &guestbook_main() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'guestbook_emoticons_list') { &guestbook_emoticons_list() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'guestbook_new_entry') {
    $submit{'guestbook'}{'new_entry'}{'name'} = $query->param ('guestbook_new_entry_name_submit');
    $submit{'guestbook'}{'new_entry'}{'email'} = $query->param ('guestbook_new_entry_email_submit');
    $submit{'guestbook'}{'new_entry'}{'website'} = $query->param ('guestbook_new_entry_website_submit');
    $submit{'guestbook'}{'new_entry'}{'message'} = $query->param ('guestbook_new_entry_message_submit');

    &guestbook_new_entry();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_interface_login_form') { &admin_interface_login_form() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_interface') {
    $submit{'admin'}{'interface_login_form'}{'uid'} = $query->param ('admin_interface_login_uid_submit');
    $submit{'admin'}{'interface_login_form'}{'password'} = $query->param ('admin_interface_login_password_submit');

    &admin_interface();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_edit_banned_words_form') { &admin_edit_banned_words_form() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_edit_banned_words_submit') {
    $submit{'admin'}{'edit_banned_words'}{'action'} = $query->param ('admin_edit_banned_words_action');
    $submit{'admin'}{'edit_banned_words'}{'new_banned_word'} = $query->param ('admin_new_banned_word_submit');
    $submit{'admin'}{'edit_banned_words'}{'del_banned_word'} = $query->param ('admin_del_banned_word_submit');

    &admin_edit_banned_words_submit();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_edit_banned_ips_form') { &admin_edit_banned_ips_form() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_edit_banned_ips_submit') {
    $submit{'admin'}{'edit_banned_ips'}{'action'} = $query->param ('admin_edit_banned_ips_action');
    $submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'} = $query->param ('admin_new_banned_ip_submit');
    $submit{'admin'}{'edit_banned_ips'}{'del_banned_ip'} = $query->param ('admin_del_banned_ip_submit');

    &admin_edit_banned_ips_submit();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_edit_gb_entry_form') { &admin_edit_gb_entry_form() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_edit_gb_entry_submit') {
    $submit{'admin'}{'edit_gb_entry'}{'time'} = $query->param ('admin_edit_gb_entry_time_submit');
    $submit{'admin'}{'edit_gb_entry'}{'ip'} = $query->param ('admin_edit_gb_entry_ip_submit');
    $submit{'admin'}{'edit_gb_entry'}{'name'} = $query->param ('admin_edit_gb_entry_name_submit');
    $submit{'admin'}{'edit_gb_entry'}{'email'} = $query->param ('admin_edit_gb_entry_email_submit');
    $submit{'admin'}{'edit_gb_entry'}{'website'} = $query->param ('admin_edit_gb_entry_website_submit');
    $submit{'admin'}{'edit_gb_entry'}{'message'} = $query->param ('admin_edit_gb_entry_message_submit');
    $submit{'admin'}{'edit_gb_entry'}{'comment'} = $query->param ('admin_edit_gb_entry_comment_submit');

    &admin_edit_gb_entry_submit();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_comment_gb_entry_form') { &admin_comment_gb_entry_form() }
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_comment_gb_entry_submit') {
    $submit{'admin'}{'comment_gb_entry'}{'comment'} = $query->param ('admin_comment_gb_entry_comment_submit');

    &admin_comment_gb_entry_submit();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_delete_gb_entry') {
    $submit{'admin'}{'delete_gb_entry'}{'flag_final'} = $query->param ('admin_delete_gb_entry_final');

    &admin_delete_gb_entry();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_ping_gb_entry') {
    $submit{'admin'}{'ping_gb_entry'}{'gb_entry_ip'} = $query->param ('admin_gb_entry_ip_submit');
    $submit{'admin'}{'ping_gb_entry'}{'gb_entry_author'} = $query->param ('admin_gb_entry_name_submit');
    &admin_ping_gb_entry();
}
elsif ($submit{'general'}{'mode'}{'action'} eq 'admin_interface_logout') { &admin_interface_logout() }







##########
# SECTION: Guestbook
####################

#=================================================
# SECTION 'Guestbook' / SUBSECTION 'general': main
#=================================================


sub guestbook_main {
    if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
        &admin_validate_session();
    }

    my @status_messages = @_;

    $html{'guestbook_main'}{'template'} = &general_parse_template ($config{'template'}{'guestbook'}{'main'});

    $html{'guestbook_main'}{'header'} = $html{'guestbook_main'}{'template'};
    $html{'guestbook_main'}{'new_entry_form'} = $html{'guestbook_main'}{'template'};
    $html{'guestbook_main'}{'navigation_status_list'} = $html{'guestbook_main'}{'template'};
    $html{'guestbook_main'}{'entries_list'} = $html{'guestbook_main'}{'template'};
    $html{'guestbook_main'}{'navigate_links'} = $html{'guestbook_main'}{'template'};
    $html{'guestbook_main'}{'footer'} = $html{'guestbook_main'}{'template'};
    delete $html{'guestbook_main'}{'template'};

    $html{'guestbook_main'}{'header'} =~ s/\n/newline/g;
    $html{'guestbook_main'}{'header'} =~ s/(.*?<body.*?>).*/$1/i;
    $html{'guestbook_main'}{'header'} =~ s/newline/\n/g;

    $html{'guestbook_main'}{'new_entry_form'} =~ s/\n/newline/g;
    $html{'guestbook_main'}{'new_entry_form'} =~ s/.*?<body.*?>(.*?<\/form.*?>).*/$1/i;
    $html{'guestbook_main'}{'new_entry_form'} =~ s/newline/\n/g;

    $html{'guestbook_main'}{'navigation_status_list'} =~ s/\n/newline/g;
    $html{'guestbook_main'}{'navigation_status_list'} =~ s/.*?<body.*?>.*?<\/form.*?>(.*?<\/tr.*?>.*?<\/tr.*?>).*/$1/i;
    $html{'guestbook_main'}{'navigation_status_list'} =~ s/newline/\n/g;

    $html{'guestbook_main'}{'entries_list'} =~ s/\n/newline/g;
    $html{'guestbook_main'}{'entries_list'} =~ s/.*?<body.*?>.*?<\/form.*?>.*?<\/tr.*?>.*?<\/tr.*?>(.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>.*?<\/tr.*?>).*/$1/i;
    $html{'guestbook_main'}{'entries_list'} =~ s/newline/\n/g;

    $html{'guestbook_main'}{'navigate_links'} =~ s/\n/newline/g;
    $html{'guestbook_main'}{'navigate_links'} =~ s/.*?<admin_navigate_links>(.*?)<\/admin_navigate_links>.*/$1/i;
    $html{'guestbook_main'}{'navigate_links'} =~ s/newline/\n/g;

    $html{'guestbook_main'}{'footer'} =~ s/\n/newline/g;
    $html{'guestbook_main'}{'footer'} =~ s/.*?(<\/body.*?>.*)/$1/i;
    $html{'guestbook_main'}{'footer'} =~ s/newline/\n/g;

    $html{'guestbook_main'}{'header'} = &general_parse_site_titles ($html{'guestbook_main'}{'header'});

    print "Content-type: text/html\n\n";
    print $html{'guestbook_main'}{'header'};
    delete $html{'guestbook_main'}{'header'};

    $html{'guestbook_main'}{'new_entry_form'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/ig;

    if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$ADMIN_INTERFACE_MODE_TAG_INVISIBLE/<input type="hidden" name="admin_interface_mode" value="1">/i;
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$ADMIN_SID_TAG_INVISIBLE/<input type="hidden" name="sid" value="$submit{'admin'}{'security'}{'sid'}">/i;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$ADMIN_INTERFACE_MODE_TAG_INVISIBLE//i;
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$ADMIN_SID_TAG_INVISIBLE//i;
    }

    if (length $submit{'guestbook'}{'new_entry'}{'name'}) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_NAME_SUBMIT/$submit{'guestbook'}{'new_entry'}{'name'}/i;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_NAME_SUBMIT//i;
    }

    if (length $submit{'guestbook'}{'new_entry'}{'email'}) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_EMAIL_SUBMIT/$submit{'guestbook'}{'new_entry'}{'email'}/i;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_EMAIL_SUBMIT//i;
    }

    if (length $submit{'guestbook'}{'new_entry'}{'website'}) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_WEBSITE_SUBMIT/$submit{'guestbook'}{'new_entry'}{'website'}/i;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_WEBSITE_SUBMIT//i;
    }

    if (length $submit{'guestbook'}{'new_entry'}{'message'}) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_MESSAGE_SUBMIT/$submit{'guestbook'}{'new_entry'}{'message'}/i;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$NEW_ENTRY_MESSAGE_SUBMIT//i;
    }

    if ($config{'setting'}{'guestbook'}{'html_mode'} == 1) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$GUESTBOOK_HTML_MODE/$config{'description'}{'guestbook'}{'html_mode_enabled'}/;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$GUESTBOOK_HTML_MODE/$config{'description'}{'guestbook'}{'html_mode_disabled'}/;
    }

    if ($config{'setting'}{'guestbook'}{'emoticons_mode'} == 1) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$GUESTBOOK_EMOTICONS_MODE/$config{'description'}{'guestbook'}{'emoticons_mode_enabled'}/;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$GUESTBOOK_EMOTICONS_MODE/$config{'description'}{'guestbook'}{'emoticons_mode_disabled'}/;
    }

    if (scalar @status_messages > 0) {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$STATUS_MESSAGES/@status_messages/;
    } else {
        $html{'guestbook_main'}{'new_entry_form'} =~ s/\$STATUS_MESSAGES//;
    }

    $html{'guestbook_main'}{'new_entry_form'} = &general_parse_buttons ($html{'guestbook_main'}{'new_entry_form'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'general'}{'new_entry'}");

    print $html{'guestbook_main'}{'new_entry_form'};
    delete $html{'guestbook_main'}{'new_entry_form'};




    $html{'guestbook_main'}{'navigation_status_list'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;

    if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
        $html{'guestbook_main'}{'navigation_status_list'} =~ s/\$ADMIN_INTERFACE_ACCESS_CONTROL/<a href="$config{'url'}{'script'}?action=admin_interface_logout&sid=$submit{'admin'}{'security'}{'sid'}">logout<\/a>/i;
    } else {
        $html{'guestbook_main'}{'navigation_status_list'} =~ s/\$ADMIN_INTERFACE_ACCESS_CONTROL/<a href="$config{'url'}{'script'}?action=admin_interface_login_form&admin_interface_mode=1">login<\/a>/i;
    }

    open (FILE_GB_ENTRIES, "<$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 0);
    my $counter_gb_entries = 0;
    while ( ! eof(FILE_GB_ENTRIES) ) {
        my $line_crap = <FILE_GB_ENTRIES>;
        if ( $line_crap =~ /\w+/) { $counter_gb_entries++ }
    }
    close (FILE_GB_ENTRIES) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 0);

    my %message = ();
    if ($counter_gb_entries <= 0) {
        $message{'guestbook'}{'counter_guestbook_entries'} = $config{'description'}{'guestbook'}{'counter_none_guestbook_entries'};
    } elsif ($counter_gb_entries == 1) {
        $message{'guestbook'}{'counter_guestbook_entries'} = "1 $config{'description'}{'guestbook'}{'counter_guestbook_entry'}";
    } elsif ($counter_gb_entries > 1) {
        $message{'guestbook'}{'counter_guestbook_entries'} = "$counter_gb_entries $config{'description'}{'guestbook'}{'counter_guestbook_entries'}";
    }

    $html{'guestbook_main'}{'navigation_status_list'} =~ s/\$MESSAGE_COUNTER_GB_ENTRIES/$message{'guestbook'}{'counter_guestbook_entries'}/i;
    delete $message{'guestbook'}{'counter_guestbook_entries'};


    $html{'admin_interface'}{'navigation_links'} = &general_parse_template ($config{'template'}{'admin'}{'interface_navigation_links'});
    $html{'admin_interface'}{'navigation_links'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/ig;
    $html{'admin_interface'}{'navigation_links'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/ig;

    if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
        $html{'guestbook_main'}{'navigation_status_list'} =~ s/\$ADMIN_INTERFACE_NAVIGATION_LINKS/$html{'admin_interface'}{'navigation_links'}/i;
    } else {
        $html{'guestbook_main'}{'navigation_status_list'} =~ s/\$ADMIN_INTERFACE_NAVIGATION_LINKS//;
    }
    delete $html{'admin_interface'}{'navigation_links'};

    print $html{'guestbook_main'}{'navigation_status_list'};
    delete $html{'guestbook_main'}{'navigation_status_list'};




    my ($count_gb_entries_displayed,
        $count_gb_entries_jump,
        $gb_entry_index,
        $gb_entry_index_start);

    open (FILE_GB_ENTRIES, "<$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $_, 0);

    while ($count_gb_entries_jump < $submit{'general'}{'guestbook_entry'}{'start_id'}) {
        my $line_crap = <FILE_GB_ENTRIES>;

        $count_gb_entries_jump++;
        $gb_entry_index++;
    }
    $gb_entry_index--;
	
    while ( ($count_gb_entries_displayed < $config{'setting'}{'guestbook'}{'entries_max_page'}) && (! eof (FILE_GB_ENTRIES) ) ) {
        my $gb_single_entry = <FILE_GB_ENTRIES>;
        next unless $gb_single_entry =~ /\w+/;
        chomp ($gb_single_entry);
        @gb_single_entry = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_single_entry);

        my @gb_entry_time = &guestbook_parse_time ($gb_single_entry[0]);

        $gb_entry_index++;

        $count_gb_entries_displayed++;

        $html{'guestbook_main'}{'entries_list_local'} = $html{'guestbook_main'}{'entries_list'};

        $html{'admin_gb_entries'}{'control_links'} = &general_parse_template ($config{'template'}{'admin'}{'guestbook_entries_control_links'});
        $html{'admin_gb_entries'}{'control_links'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/ig;
        $html{'admin_gb_entries'}{'control_links'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/ig;
        $html{'admin_gb_entries'}{'control_links'} =~ s/\$GUESTBOOK_ENTRY_ID/$gb_entry_index/ig;

        $html{'admin_gb_entries'}{'control_links'} = &general_parse_buttons ($html{'admin_gb_entries'}{'control_links'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'edit_entry'}","$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'comment_entry'}","$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'delete_entry'}");

        if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$ADMIN_GB_ENTRIES_CONTROL_LINKS/$html{'admin_gb_entries'}{'control_links'}/i;
        } else {
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$ADMIN_GB_ENTRIES_CONTROL_LINKS//i;
        }
        delete $html{'admin_gb_entries'}{'control_links'};

        $gb_single_entry[2] = &guestbook_entry_parse ($gb_single_entry[2], 'load');
        $gb_single_entry[3] = &guestbook_entry_parse ($gb_single_entry[3], 'load');
        $gb_single_entry[4] = &guestbook_entry_parse ($gb_single_entry[4], 'load');
        $gb_single_entry[5] = &guestbook_entry_parse ($gb_single_entry[5], 'load');

        $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_IDENTIFIER/<a href=mailto:$gb_single_entry[3]>$gb_single_entry[2]<\/a>/i;

        $html{'admin'}{'link_ping'} = &general_parse_template ($config{'template'}{'admin'}{'ping_link'});

        $html{'admin'}{'link_ping'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;
        $html{'admin'}{'link_ping'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/i;
        $html{'admin'}{'link_ping'} =~ s/\$ADMIN_GB_ENTRY_NAME_SUBMIT/$gb_single_entry[2]/i;
        $html{'admin'}{'link_ping'} =~ s/\$ADMIN_GB_ENTRY_IP_SUBMIT/$gb_single_entry[1]/i;

        if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$ADMIN_GB_ENTRY_PING_LINK/$html{'admin'}{'link_ping'}/i;
        } else {
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$ADMIN_GB_ENTRY_PING_LINK//i;
        }
        delete $html{'admin'}{'link_ping'};

        if ($gb_single_entry[4] !~ /http:\/\//) { $gb_single_entry[4] = "http://$gb_single_entry[4]" }
        $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_WEBSITE/$gb_single_entry[4]/ig;

        $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_TIME/$gb_entry_time[3].$gb_entry_time[4].$gb_entry_time[5] - $gb_entry_time[2].$gb_entry_time[1] $gb_entry_time[9]/i;

        $gb_single_entry[5] = &guestbook_parse_banned_words ($gb_single_entry[5]);
        $gb_single_entry[5] = &guestbook_parse_emoticons ($gb_single_entry[5]);

        $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_MESSAGE/$gb_single_entry[5]/i;

        my ($gb_entry_comment, $gb_entry_comment_time) = split (/$config{'setting'}{'guestbook'}{'dbase_subvalue_separator'}/, $gb_single_entry[7]);
        $gb_entry_comment = &guestbook_entry_parse ($gb_entry_comment, 'load', 'parse_subvalue_sep');

        if (length ($gb_entry_comment) > 0) {
            my @gb_entry_comment_time = &guestbook_parse_time ($gb_entry_comment_time);

            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_COMMENT/$gb_entry_comment/i;
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_COMMENT_FOOTER/$config{'description'}{'guestbook'}{'entry_comment_footer'}/i;
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_COMMENT_TIME/$gb_entry_comment_time[3].$gb_entry_comment_time[4].$gb_entry_comment_time[5] - $gb_entry_comment_time[2].$gb_entry_comment_time[1] $gb_entry_comment_time[9]/i;
        } else {
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_COMMENT//i;
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_COMMENT_FOOTER//i;
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_COMMENT_TIME//i;
        }

        if (length ($gb_single_entry[6]) > 0) {
            my @gb_entry_time = &guestbook_parse_time ($gb_single_entry[6]);

            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_EDIT_STATUS_FOOTER/$config{'description'}{'guestbook'}{'entry_edit_footer'}/i;
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_EDIT_STATUS_TIME/$gb_entry_time[3].$gb_entry_time[4].$gb_entry_time[5] - $gb_entry_time[2].$gb_entry_time[1] $gb_entry_time[9]/i;
        } else {
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_EDIT_STATUS_FOOTER//i;
            $html{'guestbook_main'}{'entries_list_local'} =~ s/\$GB_ENTRY_EDIT_STATUS_TIME//i;
        }
		
        print $html{'guestbook_main'}{'entries_list_local'};
    }
    delete $html{'guestbook_main'}{'entries_list_local'};

    close (FILE_GB_ENTRIES) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 0);

    my $count_gb_entries_next_page = $submit{'general'}{'guestbook_entry'}{'start_id'} + $config{'setting'}{'guestbook'}{'entries_max_page'};
    my $count_gb_entries_previous_page = $submit{'general'}{'guestbook_entry'}{'start_id'} - $config{'setting'}{'guestbook'}{'entries_max_page'};

    if ($submit{'general'}{'guestbook_entry'}{'start_id'} == 0) {
        $html{'guestbook_main'}{'navigate_links'} =~ s/\$GB_ENTRIES_NAVIGATE_LINK_PREVIOUS/$config{'description'}{'guestbook'}{'entries_navigate_link_previous_no_target'}/i;
    } else {
        if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
            $html{'guestbook_main'}{'navigate_links'} =~ s/\$GB_ENTRIES_NAVIGATE_LINK_PREVIOUS/<a href="$SCRIPT_URL_INVISIBLE?guestbook_entry_start_id=$count_gb_entries_previous_page&admin_interface_mode=1&sid=$submit{'admin'}{'security'}{'sid'}">$config{'description'}{'guestbook'}{'entries_navigate_link_previous_target'}<\/a>/i;
        } else {
            $html{'guestbook_main'}{'navigate_links'} =~ s/\$GB_ENTRIES_NAVIGATE_LINK_PREVIOUS/<a href="$SCRIPT_URL_INVISIBLE?guestbook_entry_start_id=$count_gb_entries_previous_page">$config{'description'}{'guestbook'}{'entries_navigate_link_previous_target'}<\/a>/i;
        }
    }

    if ( ($submit{'general'}{'guestbook_entry'}{'start_id'} + $config{'setting'}{'guestbook'}{'entries_max_page'}) >= $counter_gb_entries) {
        $html{'guestbook_main'}{'navigate_links'} =~     s/\$GB_ENTRIES_NAVIGATE_LINK_NEXT/$config{'description'}{'guestbook'}{'entries_navigate_link_next_no_target'}/i;
    } else {
        if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
            $html{'guestbook_main'}{'navigate_links'} =~ s/\$GB_ENTRIES_NAVIGATE_LINK_NEXT/<a href="$SCRIPT_URL_INVISIBLE?guestbook_entry_start_id=$count_gb_entries_next_page&admin_interface_mode=1&sid=$submit{'admin'}{'security'}{'sid'}">$config{'description'}{'guestbook'}{'entries_navigate_link_next_target'}<\/a>/i;
        } else {
            $html{'guestbook_main'}{'navigate_links'} =~ s/\$GB_ENTRIES_NAVIGATE_LINK_NEXT/<a href="$SCRIPT_URL_INVISIBLE?guestbook_entry_start_id=$count_gb_entries_next_page">$config{'description'}{'guestbook'}{'entries_navigate_link_next_target'}<\/a>/i;
        }
    }

    my $script_name = 'Guestbook v.0.3b';
    my $author_home_url = 'http://www.accognoscere.org';
    $html{'guestbook_main'}{'navigate_links'} =~ s/\$SCRIPT_NAME/$script_name/i;
    $html{'guestbook_main'}{'navigate_links'} =~ s/\$AUTHOR_HOME_URL/$author_home_url/i;

    print $html{'guestbook_main'}{'navigate_links'};
    print $html{'guestbook_main'}{'footer'};
    delete $html{'guestbook_main'}{'navigate_links'};
    delete $html{'guestbook_main'}{'footer'};

    exit (0);
}




#==================================================
# SECTION 'Guestbook' / SUBSECTION 'general': parse
#==================================================

sub guestbook_parse_time {
    my $time = shift (@_);
    my @time = localtime ($time);

    $time[4]++;
    $time[5] += 1900;

    if (length ($time[0]) < 2) { $time[0] = "0$time[0]" }
    if (length ($time[1]) < 2) { $time[1] = "0$time[1]" }
    if (length ($time[2]) < 2) { $time[2] = "0$time[2]" }
    if (length ($time[3]) < 2) { $time[3] = "0$time[3]" }
    if (length ($time[4]) < 2) { $time[4] = "0$time[4]" }

    my $time_period;
    if ($time[2] <= 12) {
        $time_period = $config{'description'}{'general'}{'time_period_am'};
    } else {
        $time_period = $config{'description'}{'general'}{'time_period_pm'};
    }

    push (@time, $time_period);
    return @time;
}




sub guestbook_parse_emoticons {
    my $string = shift (@_);

    if ($config{'setting'}{'guestbook'}{'emoticons_mode'} == 1) {
        $string =~ s/\>:\(/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'mad'}">/ig;
        $string =~ s/:\)/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'general'}">/ig;
        $string =~ s/\;\)/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'smile4'}">/ig;
        $string =~ s/\?\?\?/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'confused'}">/ig;
        $string =~ s/:D/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'big_grin'}">/ig;
        $string =~ s/8\)/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'cool'}">/ig;
        $string =~ s/:\~\(/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'crying'}">/ig;
        $string =~ s/:\(/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'sad'}">/ig;
        $string =~ s/:eyes/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'eyes'}">/ig;
        $string =~ s/:o/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'redface'}">/ig;
        $string =~ s/:p/<img src=\"$config{'dir'}{'emoticons'}\/$config{'image'}{'emoticon'}{'tongue'}">/ig;
    }

    return $string;
}




sub guestbook_parse_banned_words {
    my $string = shift (@_);

    if ($config{'setting'}{'guestbook'}{'replace_banned_words_mode'} == 1) {
        my @banned_words = &general_parse_file_data_array ($config{'file'}{'admin'}{'banned_words'});

        foreach my $banned_word (@banned_words) {
            chomp ($banned_word);

            if ($string =~ /$banned_word/i) {
                my $banned_word_replacor = $config{'setting'}{'guestbook'}{'replacing_item_banned_words'} x length ($banned_word);

                $string =~ s/\n/newline/g;
                $string =~ s/$banned_word/$banned_word_replacor/ig;
                $string =~ s/newline/\n/g;
            }
        }
    }

    return $string;
}




#===================================================
# SECTION 'Guestbook' / SUBSECTION 'list': emoticons
#===================================================

sub guestbook_emoticons_list {
    $html{'guestbook'}{'emoticons_list'} = &general_parse_template ($config{'template'}{'guestbook'}{'emoticons_list'});
    $html{'guestbook'}{'emoticons_list'} = &general_parse_site_titles ($html{'guestbook'}{'emoticons_list'});

    $html{'guestbook'}{'emoticons_list'} =~ s/\$DIR_EMOTICONS/$config{'dir'}{'emoticons'}/ig;

    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_GENERAL/$config{'image'}{'emoticon'}{'general'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_BIGGRIN/$config{'image'}{'emoticon'}{'big_grin'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_CONFUSED/$config{'image'}{'emoticon'}{'confused'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_COOL/$config{'image'}{'emoticon'}{'cool'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_SAD/$config{'image'}{'emoticon'}{'sad'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_CRYING/$config{'image'}{'emoticon'}{'crying'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_EYES/$config{'image'}{'emoticon'}{'eyes'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_REDFACE/$config{'image'}{'emoticon'}{'redface'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_MAD/$config{'image'}{'emoticon'}{'mad'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_SMILE4/$config{'image'}{'emoticon'}{'smile4'}/i;
    $html{'guestbook'}{'emoticons_list'} =~ s/\$IMAGE_EMOTICON_TONGUE/$config{'image'}{'emoticon'}{'tongue'}/i;

    print "Content-type: text/html\n\n";
    print $html{'guestbook'}{'emoticons_list'};
    delete $html{'guestbook'}{'emoticons_list'};

    exit (0);
}




#====================================================
# SECTION 'Guestbook' / SUBSECTION 'new entry': calls
#====================================================

sub guestbook_new_entry {
    &guestbook_new_entry_check_ip_bans();
    &guestbook_new_entry_check_form();
    &guestbook_new_entry_check_spam();
    $submit{'guestbook'}{'new_entry'}{'message'} = &guestbook_entry_parse ($submit{'guestbook'}{'new_entry'}{'message'}, 'save');
    &guestbook_new_entry_create_entry();
    &guestbook_notifying_email ('notify_admin_new_user_entry');
    &guestbook_main ($config{'message'}{'guestbook_new_entry'}{'created_successfully'});
}




#====================================================
# SECTION 'Guestbook' / SUBSECTION 'new entry': check
#====================================================

sub guestbook_new_entry_check_ip_bans {
    my @banned_ips = &general_parse_file_data_array ($config{'file'}{'admin'}{'banned_ips'});

    my $remote_ip = $ENV{'REMOTE_ADDR'};
    foreach my $banned_ip (@banned_ips) {
        chomp ($banned_ip);
        if ($remote_ip eq $banned_ip) {
            &guestbook_main ($config{'message'}{'guestbook_new_entry'}{'ip_banned'});
        }
    }
}




sub guestbook_new_entry_check_spam {
    open (GB_ENTRIES_TRACK_SPAM, "<$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}", $!, 1);
    my $gb_entry_track = <GB_ENTRIES_TRACK_SPAM>;
    my ($saved_gb_entry_time, $saved_gb_entry_ip) = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_entry_track);
    close (GB_ENTRIES_TRACK_SPAM) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}", $!, 1);

    my $current_time = time;
    my $delayed_time = ($current_time - $saved_gb_entry_time) / 60;

    my $remote_ip = $ENV{'REMOTE_ADDR'};

    if ( ($remote_ip == $saved_gb_entry_ip) && ($delayed_time < $config{'setting'}{'guestbook'}{'spam_border_time'}) ) {
        &guestbook_main ($config{'message'}{'guestbook_new_entry'}{'spam_detected'});
    }

    my @gb_entries_track_spam = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries_track_spam'});

    for (my $gb_entries_track_index = 0; $gb_entries_track_index < scalar @gb_entries_track_spam; $gb_entries_track_index++) {
        my ($gb_entry_tracked_time, $gb_entry_tracked_ip) = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_entries_track_spam[$gb_entries_track_index]);

        if ($gb_entry_tracked_ip =~ /$remote_ip/) { splice (@gb_entries_track_spam, $gb_entries_track_index, 1) }
    }

    open (ENTRIES_TRACK_SPAM, ">$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}", $!, 1);
    print ENTRIES_TRACK_SPAM "$current_time$config{'setting'}{'guestbook'}{'dbase_value_separator'}$remote_ip\n";
    close (ENTRIES_TRACK_SPAM) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}", $!, 1);

    if ($config{'setting'}{'guestbook'}{'limit_entries_track_mode'} == 1 && (scalar @gb_entries_track_spam >= $config{'setting'}{'guestbook'}{'track_entries_limit'}) ) {
        do {
            pop (@gb_entries_track_spam);
        } until ( (scalar @gb_entries_track_spam) < $config{'setting'}{'guestbook'}{'track_entries_limit'});
    }

    open (ENTRIES_TRACK_SPAM, ">>$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}", $!, 1);
    print ENTRIES_TRACK_SPAM @gb_entries_track_spam;
    close (ENTRIES_TRACK_SPAM) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries_track_spam'}", $!, 1);
}




sub guestbook_new_entry_check_form {
    my @error_messages;

    unless ( $submit{'guestbook'}{'new_entry'}{'name'} =~ /\w+/ ) {
        push (@error_messages, "$config{'message'}{'guestbook_new_entry'}{'name_missing'}$config{'setting'}{'guestbook'}{'html_breakline'}\n");
    }

    unless ( $submit{'guestbook'}{'new_entry'}{'email'} =~ /\w+/ ) {
        push (@error_messages, "$config{'message'}{'guestbook_new_entry'}{'email_missing'}$config{'setting'}{'guestbook'}{'html_breakline'}\n");
    }
    if ( $submit{'guestbook'}{'new_entry'}{'email'} =~ /\w+/ && $submit{'guestbook'}{'new_entry'}{'email'} !~ /\w+\@\w+\..{2,}/) {
        push (@error_messages, "$config{'message'}{'guestbook_new_entry'}{'email_invalid_format'}$config{'setting'}{'guestbook'}{'html_breakline'}\n");
    }

    unless ( $submit{'guestbook'}{'new_entry'}{'website'} =~ /\w+/ ) {
        push (@error_messages, "$config{'message'}{'guestbook_new_entry'}{'website_missing'}$config{'setting'}{'guestbook'}{'html_breakline'}\n");
    }
    if ( $submit{'guestbook'}{'new_entry'}{'website'} =~ /\w+/ && ($submit{'guestbook'}{'new_entry'}{'website'} !~ /\w+\.\w{2,}/ || $submit{'guestbook'}{'new_entry'}{'website'} =~ /\@/) ) {
        push (@error_messages, "$config{'message'}{'guestbook_new_entry'}{'website_invalid_format'}$config{'setting'}{'guestbook'}{'html_breakline'}\n");
    }

    unless (length $submit{'guestbook'}{'new_entry'}{'message'} > 0) {
        push (@error_messages, "$config{'message'}{'guestbook_new_entry'}{'message_missing'}$config{'setting'}{'guestbook'}{'html_breakline'}\n");
    }

    if (scalar @error_messages > 0) {
        &guestbook_main (@error_messages);
    }
}




#====================================================
# SECTION 'Guestbook' / SUBSECTION 'new entry': parse
#====================================================

sub guestbook_entry_parse {
    my $string = shift (@_);
    my $parsing_mode = shift (@_);
    my $parsing_mode_add_1 = shift (@_);

    if ($parsing_mode_add_1 eq 'parse_subvalue_sep') {
        if ($parsing_mode eq 'load' || $parsing_mode eq 'load_form') {
            $string =~ s/asc01/$config{'setting'}{'guestbook'}{'dbase_subvalue_separator'}/ig;
        } elsif ($parsing_mode eq 'save') {
            $string =~ s/$config{'setting'}{'guestbook'}{'dbase_subvalue_separator'}/asc01/ig;
        }
    }

    if ($parsing_mode eq 'save') {
        unless ($config{'setting'}{'guestbook'}{'html_mode'}) {
            $string =~ s/<.*?>//g;
        }

        my $html_breakline = $config{'setting'}{'guestbook'}{'html_breakline'};
        $string =~ s/\r\n/$html_breakline/g;
        $string =~ s/\n/$html_breakline/g;

        $string =~ s/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/asc00/ig;
    } elsif ($parsing_mode eq 'load_form') {
        $string =~ s/$config{'setting'}{'guestbook'}{'html_breakline'}/\n/ig;

        $string =~ s/asc00/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/ig;
    } elsif ($parsing_mode eq 'load') {
        $string =~ s/asc00/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/ig;
    }

    return $string;
}




#=====================================================
# SECTION 'Guestbook' / SUBSECTION 'new entry': create
#=====================================================

my ($guestbook_new_entry_time, $guestbook_new_entry_ip);
sub guestbook_new_entry_create_entry {
    $guestbook_new_entry_time = time;
    $guestbook_new_entry_ip = $ENV{'REMOTE_ADDR'};

    my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

    $submit{'guestbook'}{'new_entry'}{'name'} = &guestbook_entry_parse ($submit{'guestbook'}{'new_entry'}{'name'}, 'save');
    $submit{'guestbook'}{'new_entry'}{'email'} = &guestbook_entry_parse ($submit{'guestbook'}{'new_entry'}{'email'}, 'save');
    $submit{'guestbook'}{'new_entry'}{'website'} = &guestbook_entry_parse ($submit{'guestbook'}{'new_entry'}{'website'}, 'save');
    $submit{'guestbook'}{'new_entry'}{'message'} = &guestbook_entry_parse ($submit{'guestbook'}{'new_entry'}{'message'}, 'save');

    open (FILE_GB_ENTRIES, ">$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);
    print FILE_GB_ENTRIES "$guestbook_new_entry_time$config{'setting'}{'guestbook'}{'dbase_value_separator'}$guestbook_new_entry_ip$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'guestbook'}{'new_entry'}{'name'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'guestbook'}{'new_entry'}{'email'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'guestbook'}{'new_entry'}{'website'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'guestbook'}{'new_entry'}{'message'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}";
    unless (scalar @gb_entries == 0) { print FILE_GB_ENTRIES "\n" }
    close (FILE_GB_ENTRIES) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);

    open (FILE_GB_ENTRIES, ">>$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);
    print FILE_GB_ENTRIES @gb_entries;
    close (FILE_GB_ENTRIES) or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);
}




#=====================================================
# SECTION 'Guestbook' / SUBSECTION 'new entry': notify
#=====================================================

sub guestbook_notifying_email {
    if ($config{'setting'}{'guestbook'}{'notifying_email_mode'} == 1) {
        my $notifying_email_mode = shift (@_);
        my @notifying_email_data = @_;

        my ($email_recipient_address, $email_subject, $email_notifying_message);
        my $email_sender_adress = $config{'setting'}{'notifying_email'}{'email_address'}{'sender'};

        if ($notifying_email_mode eq 'notify_admin_new_user_entry') {
            $email_notifying_message = &guestbook_parse_notifying_email_template ($config{'template'}{'notifying_email'}{'admin_user_new_entry'}, 14);
            $email_notifying_message =~ s/(.{72}[^\n])[ \-]/$1\n/g;

            my @gb_new_entry_time = &guestbook_parse_time ($guestbook_new_entry_time);
            $email_notifying_message =~ s/\$GUESTBOOK_NEW_ENTRY_TIME/$gb_new_entry_time[3].$gb_new_entry_time[4].$gb_new_entry_time[5] - $gb_new_entry_time[2].$gb_new_entry_time[1] $gb_new_entry_time[9]/i;

            $email_notifying_message =~ s/\$GUESTBOOK_NEW_ENTRY_NAME_SUBMIT/$submit{'guestbook'}{'new_entry'}{'name'}/i;
            $email_notifying_message =~ s/\$GUESTBOOK_NEW_ENTRY_EMAIL_SUBMIT/$submit{'guestbook'}{'new_entry'}{'email'}/i;
            $email_notifying_message =~ s/\$GUESTBOOK_NEW_ENTRY_WEBSITE_SUBMIT/$submit{'guestbook'}{'new_entry'}{'website'}/i;
            $email_notifying_message =~ s/\$GUESTBOOK_NEW_ENTRY_MESSAGE_SUBMIT/$submit{'guestbook'}{'new_entry'}{'message'}/i;
            $email_notifying_message =~ s/\$GUESTBOOK_NEW_ENTRY_IP/$guestbook_new_entry_ip/i;

            undef $guestbook_new_entry_time;
            delete $submit{'guestbook'}{'new_entry'}{'name'};
            delete $submit{'guestbook'}{'new_entry'}{'email'};
            delete $submit{'guestbook'}{'new_entry'}{'website'};
            delete $submit{'guestbook'}{'new_entry'}{'message'};
            undef $guestbook_new_entry_ip;

            $email_recipient_address = $config{'setting'}{'admin'}{'email_adress'};
            $email_subject = $config{'setting'}{'notifying_email'}{'email_subject'}{'admin_new_user_entry'};
        } elsif ($notifying_email_mode eq 'notify_user_admin_comment') {
            $email_notifying_message = &guestbook_parse_notifying_email_template ($config{'template'}{'notifying_email'}{'user_admin_comment'}, 14);
            $email_notifying_message =~ s/(.{72})[ \-]/$1\n/g;
            $email_notifying_message =~ s/\$ADMIN_NAME/$config{'setting'}{'admin'}{'name'}/i;

            $email_recipient_address = $notifying_email_data[0];
            $email_subject = $config{'setting'}{'notifying_email'}{'email_subject'}{'user_admin_comment'};
        }

        open (SENDMAIL_PIPE, "| $config{'path'}{'sendmail'} -t") or &general_error ("$config{'path'}{'sendmail'} -t", $!, 1);
        print SENDMAIL_PIPE "From: $email_sender_adress\n";
        print SENDMAIL_PIPE "To: $email_recipient_address\n";
        print SENDMAIL_PIPE "Subject: $email_subject\n\n";
        print SENDMAIL_PIPE $email_notifying_message;
        close (SENDMAIL_PIPE) or &general_error ("$config{'path'}{'sendmail'} -t", $!, 1);
    }
}




sub guestbook_parse_notifying_email_template {
    my $template_notifying_email = shift (@_);
    my $template_notifying_email_lines_skip = shift (@_);

    open (TEMPLATE_NOTIFYING_EMAIL, "<$config{'dir'}{'templates'}/$template_notifying_email") or &general_error ("$config{'dir'}{'templates'}/$template_notifying_email", $!, 1);
    my @notifying_email_body = <TEMPLATE_NOTIFYING_EMAIL>;
    close (TEMPLATE_NOTIFYING_EMAIL) or &general_error ("$config{'dir'}{'templates'}/$template_notifying_email", $!, 1);

    splice (@notifying_email_body, 0, $template_notifying_email_lines_skip);

    my $notifying_email_body;
    foreach my $line (@notifying_email_body) {
        if ($line !~ /^\#/) { $notifying_email_body .= $line }
        else { last }
    }

    return $notifying_email_body;
}






##########
# SECTION: Admin interface
##########################

#=======================================================
# SECTION 'Admin interface' / SUBSECTION 'access': login
#=======================================================


sub admin_interface_login_form {
    my @status_messages = @_;

    $html{'admin'}{'interface_login_form'} = &general_parse_template ($config{'template'}{'admin'}{'interface_login_form'});

    $html{'admin'}{'interface_login_form'} = &general_parse_site_titles ($html{'admin'}{'interface_login_form'});
    $html{'admin'}{'interface_login_form'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/g;

    if (length $submit{'admin'}{'interface_login_form'}{'uid'} > 0) {
        $html{'admin'}{'interface_login_form'} =~ s/\$LOGIN_UID_SUBMIT/$submit{'admin'}{'interface_login_form'}{'uid'}/i;
    } else {
        $html{'admin'}{'interface_login_form'} =~ s/\$LOGIN_UID_SUBMIT//i;
    }

    if (length $submit{'admin'}{'interface_login_form'}{'password'} > 0) {
        $html{'admin'}{'interface_login_form'} =~ s/\$LOGIN_PASSWORD_SUBMIT/$submit{'admin'}{'interface_login_form'}{'password'}/i;
    } else {
        $html{'admin'}{'interface_login_form'} =~ s/\$LOGIN_PASSWORD_SUBMIT//i;
    }

    if (scalar @status_messages > 0) {
        $html{'admin'}{'interface_login_form'} =~ s/\$STATUS_MESSAGES/@status_messages/i;
    } else {
        $html{'admin'}{'interface_login_form'} =~ s/\$STATUS_MESSAGES//i;
    }

    $html{'admin'}{'interface_login_form'} = &general_parse_buttons ($html{'admin'}{'interface_login_form'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'login'}");

    print "Content-type: text/html\n\n";
    print $html{'admin'}{'interface_login_form'};
    delete $html{'admin'}{'interface_login_form'};

    exit (0);
}




#========================================================
# SECTION 'Admin interface' / SUBSECTION 'general': calls
#========================================================

sub admin_interface {
    if ($submit{'admin'}{'interface_login_form'}{'password'} eq $config{'setting'}{'admin'}{'interface_password'} && $submit{'admin'}{'interface_login_form'}{'uid'} eq $config{'setting'}{'admin'}{'name'}) {
        &admin_create_session();

        $submit{'general'}{'mode'}{'admin_interface'} = 1;

        &guestbook_main();
        &guestbook_navigation_status_list();
        &guestbook_entries_list();
    } else {
        my @error_messages;

	   if ($submit{'admin'}{'interface_login_form'}{'uid'} ne $config{'setting'}{'admin'}{'name'} or $submit{'admin'}{'interface_login_form'}{'password'} ne $config{'setting'}{'admin'}{'interface_password'}) {
                if ($submit{'admin'}{'interface_login_form'}{'uid'} ne $config{'setting'}{'admin'}{'name'}) {
                    push (@error_messages, "$config{'message'}{'admin_login'}{'uid_not_valid'}$config{'setting'}{'guestbook'}{'html_breakline'}");
                }
                if ($submit{'admin'}{'interface_login_form'}{'password'} ne $config{'setting'}{'admin'}{'interface_password'}) {
                    push (@error_messages, "$config{'message'}{'admin_login'}{'password_not_valid'}$config{'setting'}{'guestbook'}{'html_breakline'}");
                }
            }

       &admin_interface_login_form (@error_messages);
    }
}




#========================================================
# SECTION 'Admin interface' / SUBSECTION 'access': logout
#========================================================

sub admin_interface_logout {
    &admin_validate_session();

    open (SESSION, ">$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}") or &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);
    close (SESSION) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", 1);

    &guestbook_main();
}




#===============================================================
# SECTION 'Admin interface' / SUBSECTION 'control': banned words
#===============================================================

sub admin_edit_banned_words_form {
    &admin_validate_session();

    my $status_message = shift (@_);
    $submit{'admin'}{'edit_banned_words'}{'new_banned_word'} = $_[0];

    $html{'admin_edit_banned_words_form'}{'template'} = &general_parse_template ($config{'template'}{'admin'}{'edit_banned_words_form'});

    $html{'admin_edit_banned_words_form'}{'header'} = $html{'admin_edit_banned_words_form'}{'template'};
    $html{'admin_edit_banned_words_form'}{'body'} = $html{'admin_edit_banned_words_form'}{'template'};
    $html{'admin_edit_banned_words_form'}{'footer'} = $html{'admin_edit_banned_words_form'}{'template'};
    delete $html{'admin_edit_banned_words_form'}{'template'};

    $html{'admin_edit_banned_words_form'}{'header'} =~ s/\n/newline/g;
    $html{'admin_edit_banned_words_form'}{'header'} =~ s/(.*?<\/option.*?>).*?<\/select.*/$1/i;
    $html{'admin_edit_banned_words_form'}{'header'} =~ s/newline/\n/g;

    $html{'admin_edit_banned_words_form'}{'body'} =~ s/\n/newline/g;
    $html{'admin_edit_banned_words_form'}{'body'} =~ s/.*?<\/option.*?>(.*?)<\/select.*/$1/i;
    $html{'admin_edit_banned_words_form'}{'body'} =~ s/newline/\n/g;

    $html{'admin_edit_banned_words_form'}{'footer'} =~ s/\n/newline/g;
    $html{'admin_edit_banned_words_form'}{'footer'} =~ s/.*?(<\/select.*)/$1/i;
    $html{'admin_edit_banned_words_form'}{'footer'} =~ s/newline/\n/g;

    my @banned_words = &general_parse_file_data_array ($config{'file'}{'admin'}{'banned_words'});

    my @banned_words_2;
    foreach my $banned_word (@banned_words) {
        chomp ($banned_word);
        push (@banned_words_2, $banned_word);
    }
    @banned_words = sort @banned_words_2;
    undef @banned_words_2;

    $html{'admin_edit_banned_words_form'}{'header'} = &general_parse_site_titles ($html{'admin_edit_banned_words_form'}{'header'});
    $html{'admin_edit_banned_words_form'}{'header'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;
    $html{'admin_edit_banned_words_form'}{'header'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/i;
    $html{'admin_edit_banned_words_form'}{'header'} =~ s/\$SELECT_MSG/$config{'message'}{'admin_edit_banned_words'}{'delete_banned_word_selection'}/i;

    if (length $submit{'admin'}{'edit_banned_words'}{'new_banned_word'} > 0) {
        $html{'admin_edit_banned_words_form'}{'header'} =~ s/\$NEW_BANNED_WORD/$submit{'admin'}{'edit_banned_words'}{'new_banned_word'}/i;
    } else {
        $html{'admin_edit_banned_words_form'}{'header'} =~ s/\$NEW_BANNED_WORD//i;
    }

    print "Content-type: text/html\n\n";
    print $html{'admin_edit_banned_words_form'}{'header'};
    delete $html{'admin_edit_banned_words_form'}{'header'};

    foreach my $banned_word (@banned_words) {
    	$html{'admin_edit_banned_words_form'}{'body_local'} = $html{'admin_edit_banned_words_form'}{'body'};

    	$banned_word = &guestbook_entry_parse ($banned_word, 'load');
    	$html{'admin_edit_banned_words_form'}{'body_local'} =~ s/\$BANNED_WORD/<option value="$banned_word">$banned_word<\/option>/i;

        print $html{'admin_edit_banned_words_form'}{'body_local'};
    }
    delete $html{'admin_edit_banned_words_form'}{'body_local'};

    if (length $status_message > 0) {
        $html{'admin_edit_banned_words_form'}{'footer'} =~ s/\$STATUS_MESSAGE/$status_message/i;
    } else {
        $html{'admin_edit_banned_words_form'}{'footer'} =~ s/\$STATUS_MESSAGE//i;
    }

    $html{'admin_edit_banned_words_form'}{'footer'} = &general_parse_buttons ($html{'admin_edit_banned_words_form'}{'footer'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'general'}{'submit'}");

    print $html{'admin_edit_banned_words_form'}{'footer'};
    delete $html{'admin_edit_banned_words_form'}{'footer'};

    exit (0);
}




sub admin_edit_banned_words_submit {
    &admin_validate_session();

    my @status_messages;

    if (length $submit{'admin'}{'edit_banned_words'}{'action'} == 0) {
        &admin_edit_banned_words_form ($config{'message'}{'admin_edit_banned_words'}{'no_action_tag_submit'}, $submit{'admin'}{'edit_banned_words'}{'new_banned_word'});
    }

    if ($submit{'admin'}{'edit_banned_words'}{'action'} eq 'add' && ! $submit{'admin'}{'edit_banned_words'}{'new_banned_word'} =~ /\w+/ ) {
        &admin_edit_banned_words_form ($config{'message'}{'admin_edit_banned_words'}{'new_banned_word_not_defined'}, $submit{'admin'}{'edit_banned_words'}{'new_banned_word'});
    }

    if ($submit{'admin'}{'edit_banned_words'}{'action'} eq 'del' && $submit{'admin'}{'edit_banned_words'}{'del_banned_word'} eq $config{'message'}{'admin_edit_banned_words'}{'delete_banned_word_selection'}) {
        &admin_edit_banned_words_form ($config{'message'}{'admin_edit_banned_words'}{'delete_banned_word_no_selection'});
    }

    my $banned_words_index = 0;

    my @banned_words = &general_parse_file_data_array ($config{'file'}{'admin'}{'banned_words'});

    my @banned_words_2;
    foreach my $banned_word (@banned_words) {
            chomp ($banned_word);
            push (@banned_words_2, $banned_word);
    }

    if ( $submit{'admin'}{'edit_banned_words'}{'action'} eq 'add' && $submit{'admin'}{'edit_banned_words'}{'new_banned_word'} ne '') {
        push (@banned_words_2, $submit{'admin'}{'edit_banned_words'}{'new_banned_word'});
        push (@status_messages, $config{'message'}{'admin_edit_banned_words'}{'submit_new_banned_word_successful'});
    } elsif ($submit{'admin'}{'edit_banned_words'}{'action'} eq 'del' && $submit{'admin'}{'edit_banned_words'}{'del_banned_word'} ne '') {
        foreach my $banned_word (@banned_words_2) {
            if ($banned_word eq $submit{'admin'}{'edit_banned_words'}{'del_banned_word'}) {
                splice (@banned_words_2, $banned_words_index, 1);

                push (@status_messages, $config{'message'}{'admin_edit_banned_words'}{'delete_submit_banned_word_successful'});
                last;
            }
	
            $banned_words_index++;
        }
    }

    @banned_words_2 = sort @banned_words_2;
    undef @banned_words;

    my ($banned_words, %redundancy);
    foreach my $banned_word (@banned_words_2) {
        unless ($redundancy{$banned_word}) {
            $banned_words .= "$banned_word\n";
            $redundancy{$banned_word}++;
        }
    }

    open (BANNED_WORDS, ">$config{'dir'}{'data'}/$config{'file'}{'admin'}{'banned_words'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'banned_words'}", $!, 1);
    print BANNED_WORDS "$banned_words";
    close (BANNED_WORDS) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'banned_words'}", $!, 1);

    &admin_edit_banned_words_form (@status_messages);
}




#==============================================================
# SECTION 'Admin interface' / SUBSECTION 'control': banned IP's
#==============================================================

sub admin_edit_banned_ips_form {
    &admin_validate_session();

    my $status_message = shift (@_);

    $html{'admin_edit_banned_ips_form'}{'template'} = &general_parse_template ($config{'template'}{'admin'}{'edit_banned_ips_form'});

    $html{'admin_edit_banned_ips_form'}{'header'} = $html{'admin_edit_banned_ips_form'}{'template'};
    $html{'admin_edit_banned_ips_form'}{'body'} = $html{'admin_edit_banned_ips_form'}{'template'};
    $html{'admin_edit_banned_ips_form'}{'footer'} = $html{'admin_edit_banned_ips_form'}{'template'};
    delete $html{'admin_edit_banned_ips_form'}{'template'};

    $html{'admin_edit_banned_ips_form'}{'header'} =~ s/\n/newline/g;
    $html{'admin_edit_banned_ips_form'}{'header'} =~ s/(.*?<\/option.*?>).*?<\/select.*/$1/i;
    $html{'admin_edit_banned_ips_form'}{'header'} =~ s/newline/\n/g;

    $html{'admin_edit_banned_ips_form'}{'body'} =~ s/\n/newline/g;
    $html{'admin_edit_banned_ips_form'}{'body'} =~ s/.*?<\/option.*?>(.*?)<\/select.*/$1/i;
    $html{'admin_edit_banned_ips_form'}{'body'} =~ s/newline/\n/g;

    $html{'admin_edit_banned_ips_form'}{'footer'} =~ s/\n/newline/g;
    $html{'admin_edit_banned_ips_form'}{'footer'} =~ s/.*?(<\/select.*)/$1/i;
    $html{'admin_edit_banned_ips_form'}{'footer'} =~ s/newline/\n/g;

    my @banned_ips = &general_parse_file_data_array ($config{'file'}{'admin'}{'banned_ips'});

    my @banned_ips_2;
    foreach my $banned_ip (@banned_ips) {
        chomp ($banned_ip);
        push (@banned_ips_2, $banned_ip);
    }

    @banned_ips = sort @banned_ips_2;
    undef @banned_ips_2;

    $html{'admin_edit_banned_ips_form'}{'header'} = &general_parse_site_titles ($html{'admin_edit_banned_ips_form'}{'header'});
    $html{'admin_edit_banned_ips_form'}{'header'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;
    $html{'admin_edit_banned_ips_form'}{'header'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/i;
    $html{'admin_edit_banned_ips_form'}{'header'} =~ s/\$SELECT_MSG/$config{'message'}{'admin_edit_banned_ips'}{'delete_banned_ip_selection'}/i;

    if ( defined ($submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'}) ) {
        $html{'admin_edit_banned_ips_form'}{'header'} =~ s/\$NEW_BANNED_IP_SUBMIT/$submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'}/i;
    } else {
        $html{'admin_edit_banned_ips_form'}{'header'} =~ s/\$NEW_BANNED_IP_SUBMIT//i;
    }

    print "Content-type: text/html\n\n";
    print $html{'admin_edit_banned_ips_form'}{'header'};
    delete $html{'admin_edit_banned_ips_form'}{'header'};

    foreach my $banned_ip (@banned_ips) {
        $html{'admin_edit_banned_ips_form'}{'body_local'} = $html{'admin_edit_banned_ips_form'}{'body'};
        $html{'admin_edit_banned_ips_form'}{'body_local'} =~ s/\$BANNED_IP/<option value="$banned_ip">$banned_ip<\/option>/i;
        print $html{'admin_edit_banned_ips_form'}{'body_local'};
    }
    delete $html{'admin_edit_banned_ips_form'}{'body_local'};

    if ( defined ($status_message) ) {
        $html{'admin_edit_banned_ips_form'}{'footer'} =~ s/\$STATUS_MESSAGES/$status_message/i;
    } else {
        $html{'admin_edit_banned_ips_form'}{'footer'} =~ s/\$STATUS_MESSAGES//i;
    }

    $html{'admin_edit_banned_ips_form'}{'footer'} = &general_parse_buttons ($html{'admin_edit_banned_ips_form'}{'footer'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'general'}{'submit'}");

    print $html{'admin_edit_banned_ips_form'}{'footer'};
    delete $html{'admin_edit_banned_ips_form'}{'footer'};

    exit (0);
}




sub admin_edit_banned_ips_submit {
    &admin_validate_session();

    my @status_messages;

    unless ( defined ($submit{'admin'}{'edit_banned_ips'}{'action'}) ) {
        &admin_edit_banned_ips_form ($config{'message'}{'admin_edit_banned_ips'}{'no_action_tag_submit'});
    }

    if ($submit{'admin'}{'edit_banned_ips'}{'action'} eq 'add' && length ($submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'}) == 0) {
        &admin_edit_banned_ips_form ($config{'message'}{'admin_edit_banned_ips'}{'new_banned_ip_submit_not_defined'});
    }
    if ($submit{'admin'}{'edit_banned_ips'}{'action'} eq 'add' && $submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'} =~ /[a-z]+/i) {
        &admin_edit_banned_ips_form ($config{'message'}{'admin_edit_banned_ips'}{'new_banned_ip_invalid_format'}, $submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'});
    }
    if ($submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'} =~ /\d+/ && ($submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'} !~ /\d+\.\d+\.\d+\.\d+/) ) {
        &admin_edit_banned_ips_form ($config{'message'}{'admin_edit_banned_ips'}{'new_banned_ip_invalid_format'}, $submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'});
    }

    if ($submit{'admin'}{'edit_banned_ips'}{'action'} eq 'del' && $submit{'admin'}{'edit_banned_ips'}{'del_banned_ip'} eq $config{'message'}{'admin_edit_banned_ips'}{'delete_banned_ip_selection'}) {
        &admin_edit_banned_ips_form ($config{'message'}{'admin_edit_banned_ips'}{'delete_banned_ip_no_selection'});
    }

    my $banned_ips_index = 0;
	my (@banned_ips_2, %redundancy);

    my @banned_ips = &general_parse_file_data_array ($config{'file'}{'admin'}{'banned_ips'});

    foreach my $banned_ip (@banned_ips) {
        chomp ($banned_ip);
        push (@banned_ips_2, $banned_ip);
    }
    undef @banned_ips;

       if ($submit{'admin'}{'edit_banned_ips'}{'action'} eq 'add' && $submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'} ne '') {
        push (@banned_ips_2, $submit{'admin'}{'edit_banned_ips'}{'new_banned_ip'});

        push (@status_messages, $config{'message'}{'admin_edit_banned_ips'}{'new_banned_ip_submit_successful'});
    } elsif ( $submit{'admin'}{'edit_banned_ips'}{'action'} eq 'del' && $submit{'admin'}{'edit_banned_ips'}{'del_banned_ip'} ne '') {
        foreach my $banned_ip (@banned_ips_2) {
            if ($banned_ip eq $submit{'admin'}{'edit_banned_ips'}{'del_banned_ip'}) {
                splice (@banned_ips_2, $banned_ips_index, 1);

                undef @status_messages;
                    push (@status_messages, $config{'message'}{'admin_edit_banned_ips'}{'delete_banned_ip_submit_successful'});
                last;
            }

            $banned_ips_index++;
        }
    }

    @banned_ips_2 = sort @banned_ips_2;

    my $banned_ips;
    foreach my $banned_ip (@banned_ips_2) {
        unless ($redundancy{$banned_ip}) {
            $banned_ips .= "$banned_ip\n";
            $redundancy{$banned_ip}++;
        }
    }

    open (BANNED_IPS, ">$config{'dir'}{'data'}/$config{'file'}{'admin'}{'banned_ips'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'banned_ips'}", $!, 1);
    print BANNED_IPS $banned_ips;
    close (BANNED_IPS) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'banned_ips'}", $!, 1);

    &admin_edit_banned_ips_form (@status_messages);
}




#=======================================================
# SECTION 'Admin interface' / SUBSECTION 'control': edit
#=======================================================

sub admin_edit_gb_entry_form {
    &admin_validate_session();

    $html{'admin_edit_gb_entry'}{'form'} = &general_parse_template ($config{'template'}{'admin'}{'edit_guestbook_entry_form'});

    my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

    for (my $gb_entry_index = 0; $gb_entry_index < scalar @gb_entries; $gb_entry_index++) {
        if ($gb_entry_index eq $submit{'general'}{'guestbook_entry'}{'id'}) {
            my @gb_entry = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_entries[$gb_entry_index]);

            $gb_entry[2] = &guestbook_entry_parse ($gb_entry[2], 'load_form');
            $gb_entry[3] = &guestbook_entry_parse ($gb_entry[3], 'load_form');
            $gb_entry[4] = &guestbook_entry_parse ($gb_entry[4], 'load_form');
            $gb_entry[5] = &guestbook_entry_parse ($gb_entry[5], 'load_form');

            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_TIME/$gb_entry[0]/i;
            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_IP/$gb_entry[1]/i;
            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_NAME/$gb_entry[2]/i;
            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_EMAIL/$gb_entry[3]/i;
            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_WEBSITE/$gb_entry[4]/i;
            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_MESSAGE/$gb_entry[5]/i;
            $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GB_ENTRY_COMMENT/$gb_entry[7]/i;
        }
    }

    $html{'admin_edit_gb_entry'}{'form'} = &general_parse_site_titles ($html{'admin_edit_gb_entry'}{'form'});
    $html{'admin_edit_gb_entry'}{'form'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;
    $html{'admin_edit_gb_entry'}{'form'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/i;
    $html{'admin_edit_gb_entry'}{'form'} =~ s/\$GUESTBOOK_ENTRY_ID/$submit{'general'}{'guestbook_entry'}{'id'}/i;

    $html{'admin_edit_gb_entry'}{'form'} = &general_parse_buttons ($html{'admin_edit_gb_entry'}{'form'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'edit'}");

    print "Content-type: text/html\n\n";
    print $html{'admin_edit_gb_entry'}{'form'};
    delete $html{'admin_edit_gb_entry'}{'form'};

    exit (0);
}




sub admin_edit_gb_entry_submit {
    &admin_validate_session();

    my $current_time = time;

    my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

    for (my $gb_entry_index = 0; $gb_entry_index < scalar @gb_entries; $gb_entry_index++) {
        if ($gb_entry_index == $submit{'general'}{'guestbook_entry'}{'id'}) {
            $submit{'admin'}{'edit_gb_entry'}{'name'} = &guestbook_entry_parse ($submit{'admin'}{'edit_gb_entry'}{'name'}, 'save');
            $submit{'admin'}{'edit_gb_entry'}{'email'} = &guestbook_entry_parse ($submit{'admin'}{'edit_gb_entry'}{'email'}, 'save');
            $submit{'admin'}{'edit_gb_entry'}{'website'} = &guestbook_entry_parse ($submit{'admin'}{'edit_gb_entry'}{'website'}, 'save');
            $submit{'admin'}{'edit_gb_entry'}{'message'} = &guestbook_entry_parse ($submit{'admin'}{'edit_gb_entry'}{'message'}, 'save');

            $gb_entries[$submit{'general'}{'guestbook_entry'}{'id'}] = "$submit{'admin'}{'edit_gb_entry'}{'time'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'edit_gb_entry'}{'ip'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'edit_gb_entry'}{'name'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'edit_gb_entry'}{'email'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'edit_gb_entry'}{'website'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'edit_gb_entry'}{'message'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}$current_time$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'edit_gb_entry'}{'comment'}$config{'setting'}{'guestbook'}{'dbase_value_separator'}\n";

            last;
        }
    }

    open (FILE_GB_ENTRIES, ">$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);
    print FILE_GB_ENTRIES @gb_entries;
    close (FILE_GB_ENTRIES) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);

    &guestbook_main();
}




#==========================================================
# SECTION 'Admin interface' / SUBSECTION 'control': comment
#==========================================================

sub admin_comment_gb_entry_form {
    &admin_validate_session();

    $html{'admin_comment_gb_entry'}{'form'} = &general_parse_template ($config{'template'}{'admin'}{'comment_guestbook_entry_form'});

    $html{'admin_comment_gb_entry'}{'form'} = &general_parse_site_titles ($html{'admin_comment_gb_entry'}{'form'});
    $html{'admin_comment_gb_entry'}{'form'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;
    $html{'admin_comment_gb_entry'}{'form'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/i;
    $html{'admin_comment_gb_entry'}{'form'} =~ s/\$GUESTBOOK_ENTRY_ID/$submit{'general'}{'guestbook_entry'}{'id'}/i;

    my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

    for (my $gb_entry_index = 0; $gb_entry_index < scalar @gb_entries; $gb_entry_index++) {
        if ($gb_entry_index eq $submit{'general'}{'guestbook_entry'}{'id'}) {
            my @gb_entry = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_entries[$gb_entry_index]);

            my ($gb_entry_comment, $gb_entry_comment_time) = split (/$config{'setting'}{'guestbook'}{'dbase_subvalue_separator'}/, $gb_entry[7]);

            $gb_entry_comment = &guestbook_entry_parse ($gb_entry_comment, 'load_form', 'parse_subvalue_sep');
            $html{'admin_comment_gb_entry'}{'form'} =~ s/\$GB_ENTRY_COMMENT/$gb_entry_comment/i;
        }
    }

    $html{'admin_comment_gb_entry'}{'form'} = &general_parse_buttons ($html{'admin_comment_gb_entry'}{'form'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'comment'}");

    print "Content-type: text/html\n\n";
    print $html{'admin_comment_gb_entry'}{'form'};
    delete $html{'admin_comment_gb_entry'}{'form'};

    exit (0);
}




sub admin_comment_gb_entry_submit {
    &admin_validate_session();

    my $gb_entry_email_adress;

    my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

    for (my $gb_entry_index = 0; $gb_entry_index < scalar @gb_entries; $gb_entry_index++) {
        if ($gb_entry_index eq $submit{'general'}{'guestbook_entry'}{'id'}) {
            my @gb_entry = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_entries[$gb_entry_index]);
            $gb_entry_email_adress = $gb_entry[3];

            $submit{'admin'}{'comment_gb_entry'}{'comment'} = &guestbook_entry_parse ($submit{'admin'}{'comment_gb_entry'}{'comment'}, 'save', 'parse_subvalue_sep');

            if ($submit{'admin'}{'comment_gb_entry'}{'comment'} =~ /\w+/) {
                $gb_entry[7] = "$submit{'admin'}{'comment_gb_entry'}{'comment'}" . $config{'setting'}{'guestbook'}{'dbase_subvalue_separator'} . time;
            } else { $gb_entry[7] = '' }

            my $gb_entry;
            foreach my $item (@gb_entry) { $gb_entry .= "$item$config{'setting'}{'guestbook'}{'dbase_value_separator'}" }
            chop ($gb_entry);
            $gb_entries[$gb_entry_index] = $gb_entry;

            last;
        }
    }

    open (FILE_GB_ENTRIES, ">$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);
    print FILE_GB_ENTRIES @gb_entries;
    close (FILE_GB_ENTRIES) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);

    &guestbook_notifying_email ('notify_user_admin_comment', $gb_entry_email_adress);

    &guestbook_main();
}




#=========================================================
# SECTION 'Admin interface' / SUBSECTION 'control': delete
#=========================================================

sub admin_delete_gb_entry {
    &admin_validate_session();

    if ($config{'setting'}{'admin'}{'delete_gb_entry_verification_mode'} == 0 || $submit{'admin'}{'delete_gb_entry'}{'flag_final'} == 1) {
        my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

        splice (@gb_entries, $submit{'general'}{'guestbook_entry'}{'id'}, 1);

        open (FILE_GB_ENTRIES, ">$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);
        print FILE_GB_ENTRIES @gb_entries;
        close (FILE_GB_ENTRIES) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'guestbook'}{'entries'}", $!, 1);

        &guestbook_main();
    } else {
        my @gb_entries = &general_parse_file_data_array ($config{'file'}{'guestbook'}{'entries'});

        my $gb_single_entry = @gb_entries[$submit{'general'}{'guestbook_entry'}{'id'}];
        my @gb_single_entry = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $gb_single_entry);

        my @gb_entry_time = &guestbook_parse_time ($gb_single_entry[0]);

        $html{'admin_delete_gb_entry'}{'verification_form'} = &general_parse_template ($config{'template'}{'admin'}{'delete_guestbook_entry_verification_form'});

        $html{'admin_delete_gb_entry'}{'verification_form'} = &general_parse_site_titles ($html{'admin_delete_gb_entry'}{'verification_form'});

        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$SCRIPT_URL_INVISIBLE/$config{'url'}{'script'}/i;
        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$SID_INVISIBLE/$submit{'admin'}{'security'}{'sid'}/i;
        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GUESTBOOK_ENTRY_ID_INVISIBLE/$submit{'general'}{'guestbook_entry'}{'id'}/i;

        $gb_single_entry[2] = &guestbook_entry_parse ($gb_single_entry[2], 'load');
        $gb_single_entry[3] = &guestbook_entry_parse ($gb_single_entry[3], 'load');
        $gb_single_entry[4] = &guestbook_entry_parse ($gb_single_entry[4], 'load');
        $gb_single_entry[5] = &guestbook_entry_parse ($gb_single_entry[5], 'load');

        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_IDENTIFIER/<a href=mailto:$gb_single_entry[3]>$gb_single_entry[2]<\/a>/i;

        if ($gb_single_entry[4] !~ /http:\/\//) { $gb_single_entry[4] = "http://$gb_single_entry[4]" }
        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_WEBSITE/$gb_single_entry[4]/ig;

        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_TIME/$gb_entry_time[3].$gb_entry_time[4].$gb_entry_time[5] - $gb_entry_time[2].$gb_entry_time[1] $gb_entry_time[9]/i;

        $gb_single_entry[5] = &guestbook_parse_banned_words ($gb_single_entry[5]);
        $gb_single_entry[5] = &guestbook_parse_emoticons ($gb_single_entry[5]);

        $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_MESSAGE/$gb_single_entry[5]/i;

        my ($gb_entry_comment, $gb_entry_comment_time) = split (/$config{'setting'}{'guestbook'}{'dbase_subvalue_separator'}/, $gb_single_entry[7]);
        $gb_entry_comment = &guestbook_entry_parse ($gb_entry_comment, 'load', 'parse_subvalue_sep');

        if ($gb_entry_comment =~ /\w+/) {
            my @gb_entry_comment_time = &guestbook_parse_time ($gb_entry_comment_time);

            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_COMMENT/$gb_entry_comment/i;
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_COMMENT_FOOTER/$config{'description'}{'guestbook'}{'entry_comment_footer'}/i;
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_COMMENT_TIME/$gb_entry_comment_time[3].$gb_entry_comment_time[4].$gb_entry_comment_time[5] - $gb_entry_comment_time[2].$gb_entry_comment_time[1] $gb_entry_comment_time[9]/i;
        } else {
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_COMMENT//i;
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_COMMENT_FOOTER//i;
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_COMMENT_TIME//i;
        }

        if ($gb_single_entry[6] =~ /\d+/) {
            my @gb_entry_time = &guestbook_parse_time ($gb_single_entry[6]);

            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_EDIT_STATUS_FOOTER/$config{'description'}{'guestbook'}{'entry_edit_footer'}/i;
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_EDIT_STATUS_TIME/$gb_entry_time[3].$gb_entry_time[4].$gb_entry_time[5] - $gb_entry_time[2].$gb_entry_time[1] $gb_entry_time[9]/i;
        } else {
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_EDIT_STATUS_FOOTER//i;
            $html{'admin_delete_gb_entry'}{'verification_form'} =~ s/\$GB_ENTRY_EDIT_STATUS_TIME//i;
        }

        $html{'admin_delete_gb_entry'}{'verification_form'} = &general_parse_buttons ($html{'admin_delete_gb_entry'}{'verification_form'}, "$config{'dir'}{'buttons'}/$config{'image'}{'button'}{'admin'}{'delete'}");

        print "Content-type: text/html\n\n";
        print $html{'admin_delete_gb_entry'}{'verification_form'};
        delete $html{'admin_delete_gb_entry'}{'verification_form'};

        exit (0);
    }
}




#==================================================
# SECTION 'Admin interface' / SUBSECTION 'sessions'
#==================================================

sub admin_create_session {
    my $current_time = time;

    my $random_digit_1 = rand ($config{'setting'}{'admin'}{'session_random_digit_1'}) + 1;
    my $random_digit_2 = rand ($config{'setting'}{'admin'}{'session_random_digit_2'}) + 1;
    $submit{'admin'}{'security'}{'sid'} = $random_digit_1 * $random_digit_2;

    open (ADMIN_SESSION, ">$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);
    print ADMIN_SESSION "$current_time$config{'setting'}{'guestbook'}{'dbase_value_separator'}$submit{'admin'}{'security'}{'sid'}";
    close (ADMIN_SESSION) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);
}




sub admin_validate_session {
   open (ADMIN_SESSION, "<$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);
   my $admin_session_entry = <ADMIN_SESSION>;
   close (ADMIN_SESSION) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);

   chomp ($admin_session_entry);
   my ($admin_saved_session_time, $admin_saved_session_sid) = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $admin_session_entry);

   my $current_time = time;
   my $runtime = ($current_time - $admin_saved_session_time) / 60;

   if ( ($submit{'admin'}{'security'}{'sid'} == $admin_saved_session_sid) && ($runtime < $config{'setting'}{'admin'}{'session_runout_time_min'}) ) {
        &admin_renew_session();
   } else {
        &admin_interface_login_form ($config{'message'}{'admin'}{'session_invalid'});
   }
}




sub admin_renew_session {
    open (ADMIN_SESSION, "<$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);
    my $admin_session_entry = <ADMIN_SESSION>;
    close (ADMIN_SESSION) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);

    my @admin_session_entry = split (/$config{'setting'}{'guestbook'}{'dbase_value_separator'}/, $admin_session_entry);
    my $current_time = time;
    $admin_session_entry[0] = $current_time;
    $admin_session_entry = $admin_session_entry[0] . $config{'setting'}{'guestbook'}{'dbase_value_separator'} . $admin_session_entry[1];

    open (ADMIN_SESSION, ">$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}") || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}");
    print ADMIN_SESSION $admin_session_entry;
    close (ADMIN_SESSION) || &general_error ("$config{'dir'}{'data'}/$config{'file'}{'admin'}{'session_entries'}", $!, 1);
}




#==============================================
# SECTION 'Admin interface' / SUBSECTION 'ping'
#==============================================

sub admin_ping_gb_entry {
    &admin_validate_session();

    open (PING, "$config{'path'}{'ping'} -c1 $submit{'admin'}{'ping_gb_entry'}{'gb_entry_ip'} |") || &general_error ("$config{'path'}{'ping'}", $!, 1);
    my @ping_results = <PING>;
    close (PING) || &general_error ("$config{'path'}{'ping'}", $!, 1);

    my $guestbook_entry_author_status;
    $guestbook_entry_author_status = $config{'description'}{'guestbook'}{'entry_author_online_status'};

    foreach (@ping_results) {
        if (/0 packets received/i) {
            $guestbook_entry_author_status = $config{'description'}{'guestbook'}{'entry_author_offline_status'};
        }
    }

    $html{'admin'}{'ping_user'} = &general_parse_template ($config{'template'}{'admin'}{'ping_user'});
    $html{'admin'}{'ping_user'} = &general_parse_site_titles ($html{'admin'}{'ping_user'});

    $html{'admin'}{'ping_user'} =~ s/\$GB_ENTRY_AUTHOR_STATUS/$guestbook_entry_author_status/i;
    $html{'admin'}{'ping_user'} =~ s/\$GB_ENTRY_AUTHOR/$submit{'admin'}{'ping_gb_entry'}{'gb_entry_author'}/i;
    $html{'admin'}{'ping_user'} =~ s/\$GB_ENTRY_IP/$submit{'admin'}{'ping_gb_entry'}{'gb_entry_ip'}/i;

    print "Content-type: text/html\n\n";
    print $html{'admin'}{'ping_user'};
    delete $html{'admin'}{'ping_user'};

    exit (0);

}






##########
# SECTION: General
##################

#=======================================
# SECTION 'General' / SUBSECTION 'error'
#=======================================

sub general_error {
    my $error_path = $_[0];
    my $error_status = $_[1];
    my $print_mime_header = $_[2];

    $html{'general'}{'error'} = &general_parse_template ($config{'template'}{'general'}{'error'});

    $html{'general'}{'error'} = &general_parse_site_titles ($html{'general'}{'error'});
    $html{'general'}{'error'} =~ s/\$ERROR_PATH/$error_path/i;
    $html{'general'}{'error'} =~ s/\$ERROR_STATUS/$error_status/i;

    if ($print_mime_header == 1) {
        print "Content-type: text/html\n\n";
    }
    print $html{'general'}{'error'};
    delete $html{'general'}{'error'};

    exit (0);
}




#=====================================================
# SECTION 'General' / SUBSECTION 'parse' : site titles
#=====================================================

sub general_parse_site_titles {
    my $string = shift (@_);

    $string =~ s/\$GUESTBOOK_NAME/$config{'setting'}{'general'}{'guestbook_name'}/i;

    my $site_title;
    if ($submit{'general'}{'mode'}{'admin_interface'} == 1) {
        $site_title = $config{'setting'}{'admin'}{'site_title'};
    } else {
        $site_title = $config{'setting'}{'guestbook'}{'site_title'};
    }

    $string =~ s/\$SITE_TITLE/$site_title/i;

    return $string;
}




#=====================================================
# SECTION 'General' / SUBSECTION 'parse' : data string
#=====================================================

sub general_parse_file_data_string {
    my $file_data = shift (@_);

    open (FILE_DATA, "<$config{'dir'}{'data'}/$file_data") || &general_error ("$config{'dir'}{'data'}/$file_data", $!, 1);

    my $file_data_content;
    while (! eof(FILE_DATA) ) {
        $file_data_content .= <FILE_DATA>;
    }

    close (FILE_DATA) || &general_error ("$config{'dir'}{'data'}/$file_data", $!, 1);

    return $file_data_content;
}




#====================================================
# SECTION 'General' / SUBSECTION 'parse' : data array
#====================================================

sub general_parse_file_data_array {
    my $file_data = shift (@_);

    open (FILE_DATA, "<$config{'dir'}{'data'}/$file_data") || &general_error ("$config{'dir'}{'data'}/$file_data", $!, 1);
    my @file_data_content = <FILE_DATA>;
    close (FILE_DATA) || &general_error ("$config{'dir'}{'data'}/$file_data", $!, 1);

    return @file_data_content;
}




#==================================================
# SECTION 'General' / SUBSECTION 'parse' : template
#==================================================

sub general_parse_template {
    my $template = shift (@_);

    my $template_html;

    open (TEMPLATE, "<$config{'dir'}{'templates'}/$template") || &general_error ("$config{'dir'}{'templates'}/$template", $!, 1);
    while (! eof(TEMPLATE) ) {
        $template_html .= <TEMPLATE>;
    }
    close (TEMPLATE) || &general_error ("$config{'dir'}{'templates'}/$template", $!, 1);

    return $template_html;
}



#=================================================
# SECTION 'General' / SUBSECTION 'parse' : buttons
#=================================================

sub general_parse_buttons {
    my $string = shift (@_);
    my @absolute_path_button = @_;

    if (scalar @absolute_path_button == 1) {
        $string =~ s/\$ABSOLUTE_PATH_BUTTON/$absolute_path_button[0]/i;
    } elsif (scalar @absolute_path_button == 3) {
        $string =~ s/\$ABSOLUTE_PATH_BUTTON_1/$absolute_path_button[0]/i;
        $string =~ s/\$ABSOLUTE_PATH_BUTTON_2/$absolute_path_button[1]/i;
        $string =~ s/\$ABSOLUTE_PATH_BUTTON_3/$absolute_path_button[2]/i;
    }

    return $string;
}






__END__


BEGIN {
    $VERSION = '0.4';
    $AUTHOR = 'Steven Schubiger';
    $AUTHOR_EMAIL = 'steven@accognoscere.org' ;
}


=head1 NAME

Guestbook v.0.3b

=head1 DESCRIPTION

A highly configurable CGI-script which uses ASCII files to store
its data. While this POD manual remains more of an informative
nature, the supplied, extensive user manual may support
further information.


=head1 SCOPE

=head2 guestbook features

=over 4

=item *

Separated config file & config file creator

=item *

HTML templates & -placeholders

=item *

ASCII files to storage data & use of free definable separating-values

=item *

Graphical form buttons supportment

=item *

Syntax parsing of submitted new entrys

=item *

Splitting the guestbook entries in subpages

=item *

Emoticons & HTML support

=back

=head2 administrating features

=over 4

=item *

An password-protected administrator interface


=item *

Dynamic administrator session-ID


=item *

Ban words & IP's

=item *

Edit, comment & delete a guestbook entry

=item *

View the online status of an user

=back

=head2 general features

=over 4

=item *

Widely commented source code

=item *

An extensive user manual & reference guide

=back

=cut