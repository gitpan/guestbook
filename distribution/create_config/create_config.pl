#! /usr/local/bin/perl -w

 
#################################################################################
#										#
#                                                                               #
#   Create config v.0.01a                                     			#
#   Copyright (c) 2003-2004 by Steven Schubiger <steven@accognoscere.org>       #
#   Last changes: 12th November 2004						#
#										#		
#   All rights reserved.                                                        #
#                                                                               #                                       
#   Redistribution and use in source and binary forms, with or without          #
#   modification, are permitted provided that the following conditions          #
#   are met:                                                                    #
#   1. Redistributions of source code must retain the above copyright           #
#      notice, this list of conditions and the following disclaimer.            #
#   2. Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the      #
#      documentation and/or other materials provided with the distribution.     #
#   3. The name of the author may not be used to endorse or promote products    #
#      derived from this software without specific prior written permission.    #
#                                                                               #
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR        #
#   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES   #
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.     #
#   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,            #
#   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT    #
#   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,   #
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY       #
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT         #
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF    #
#   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.           #
#                                                                               #
#                                                                               #
#################################################################################






##########
# SECTION: CGI-Environment & global calls
#########################################

use CGI::Carp ('fatalsToBrowser');
use integer;
use strict;

my (%config_setting, $identifier, $level_identifier,
    $lines_total_input, $lines_total_output);


my $config_file_in = 'guestbook.dat';
my $config_file_out = '../guestbook.cfg';
my $template_create_config = 'template_create_config.html';


&create_config();
&output_html();






##########
# SECTION: Create config
########################

#============================================
# SECTION 'Create config' / SUBSECTION 'main'
#============================================

sub create_config {
    open (CONFIG_IN, "<$config_file_in") or die "Could not open $config_file_in for reading: $!\n";
    open (CONFIG_OUT, ">$config_file_out") or die "Could not open $config_file_out for writing: $!\n";

    my $value;
    while (! eof(CONFIG_IN) ) {
        my $line = <CONFIG_IN>;
        chomp ($line);
        $lines_total_input++;
        next unless $line =~ /^.\$/ || $line =~ /^\w+/;

        my (%config, $level_1_identifier,
            $level_2_identifier, $level_3_identifier);

        if ($line =~ /^.\$/) {
            my $level_value;

            my $line_2 = <CONFIG_IN>;
            chomp ($line_2);

            my @lines;
            push (@lines, $line);
            push (@lines, $line_2);
            undef $line;
            undef $line_2;

            my $i = 0;
            ($level_identifier, $level_value) = split (/=/, $lines[$i++]);
            ($identifier, $value) = split (/=/, $lines[$i]);

            if ($level_value == 1) {
                delete $config_setting{$level_identifier}{1}{$identifier};
                delete $config_setting{$level_identifier}{2}{$identifier};
                delete $config_setting{$level_identifier}{3}{$identifier};
            } elsif ($level_value == 2) {
                delete $config_setting{$level_identifier}{2}{$identifier};
                delete $config_setting{$level_identifier}{3}{$identifier};
            } elsif ($level_value == 3) {
                delete $config_setting{$level_identifier}{3}{$identifier};
            }

            $config_setting{$level_identifier}{$level_value}{$identifier} = $value;
        } elsif ($line =~ /^\w+/) {
            my ($identifier_user_cfg, $value_user_cfg);

            $level_1_identifier = $config_setting{$level_identifier}{1}{$identifier};
            chomp ($level_1_identifier);
            $level_2_identifier = $config_setting{$level_identifier}{2}{$identifier};
            chomp ($level_2_identifier);
            $level_3_identifier = $config_setting{$level_identifier}{3}{$identifier};
            chomp ($level_3_identifier);

            my $quoting_char = chr (34);
            if ( length ($config_setting{$level_identifier}{1}{$identifier}) > 0 && ($config_setting{$level_identifier}{2}{$identifier} !~ /\w+/ && $config_setting{$level_identifier}{3}{$identifier} !~ /\w+/) ) {
                ($identifier_user_cfg, $value_user_cfg) = split (/ = /, $line);
                $config{$level_1_identifier}{$identifier_user_cfg} = $value_user_cfg;

                my $value = " = $quoting_char$value_user_cfg$quoting_char\;\n";
                print CONFIG_OUT '$config' . "\{\'$level_1_identifier\'\}\{\'$identifier_user_cfg\'\}$value";
                $lines_total_output++;
            } elsif ( (length ($config_setting{$level_identifier}{1}{$identifier}) > 0 && length ($config_setting{$level_identifier}{2}{$identifier}) > 0) && $config_setting{$level_identifier}{3}{$identifier} !~ /\w+/) {
                ($identifier_user_cfg, $value_user_cfg) = split (/ = /, $line);
                $config{$level_1_identifier}{$level_2_identifier}{$identifier_user_cfg} = $value_user_cfg;

                my $value = " = $quoting_char$value_user_cfg$quoting_char\;\n";
                print CONFIG_OUT '$config' . "\{\'$level_1_identifier\'\}\{\'$level_2_identifier\'\}\{\'$identifier_user_cfg\'\}$value";
                $lines_total_output++;
            } elsif (length ($config_setting{$level_identifier}{1}{$identifier}) > 0 && length ($config_setting{$level_identifier}{2}{$identifier}) > 0 && length ($config_setting{$level_identifier}{3}{$identifier}) > 0) {
                ($identifier_user_cfg, $value_user_cfg) = split (/ = /, $line);
                $config{$level_1_identifier}{$level_2_identifier}{$level_3_identifier}{$identifier_user_cfg} =     $value_user_cfg;

                my $value = " = $quoting_char$value_user_cfg$quoting_char\;\n";
                print CONFIG_OUT '$config' . "\{\'$level_1_identifier\'\}\{\'$level_2_identifier\'\}\{\'$level_3_identifier\'\}\{\'$identifier_user_cfg\'\}$value";
                $lines_total_output++;
            }
        }
    }

    close (CONFIG_IN) or die "Could not close $config_file_in: $!\n";
    close (CONFIG_OUT) or die "Could not close $config_file_out: $!\n";
}




#===================================================
# SECTION 'Create config' / SUBSECTION 'output HTML'
#===================================================

sub output_html {
    my %html;
    $html{'create_config'}{'template'} = &general_parse_template ($template_create_config);

    my $runtime_sec = (time - $^T) / 60;

    $html{'create_config'}{'template'} =~ s/\$CONFIG_FILE_IN/$config_file_in/i;
    $html{'create_config'}{'template'} =~ s/\$CONFIG_FILE_OUT/$config_file_out/i;
    $html{'create_config'}{'template'} =~ s/\$LINES_TOTAL_INPUT/$lines_total_input/i;
    $html{'create_config'}{'template'} =~ s/\$LINES_TOTAL_OUTPUT/$lines_total_output/i;
    $html{'create_config'}{'template'} =~ s/\$RUNTIME_SEC/$runtime_sec/i;

    print "Content-type: text/html\n\n";
    print $html{'create_config'}{'template'};
    exit (0);
}






##########
# SECTION: General
##################

#================================================
# SECTION 'General' / SUBSECTION 'parse template'
#================================================

sub general_parse_template {
    my $template = shift (@_);

    my $template_html;

    open (TEMPLATE, "<$template") or die "Could not open $template for reading: $!\n";
    while (! eof(TEMPLATE) ) {
        $template_html .= <TEMPLATE>;
    }
    close (TEMPLATE) or die "Could not open $template for writing: $!\n";

    return $template_html;
}






__END__


BEGIN {
    $VERSION = '0.01a';
    $AUTHOR = 'Steven Schubiger';
    $AUTHOR_EMAIL = 'steven@accognoscere.org' ;
}


=head1 NAME

Create config v.0.01a

=head1 DESCRIPTION

Parses the entire user config file into an hash which subsequently is stored
within a new file & referenced by the main guestbook script.

=head1 USAGE

Has to be initally run to create a configuration file;
each time you've applied changes to the user configuration file,
the process is due again.

=head1 BUGTRACKING

If you will encounter any serious issues within the code and/or track down
some bugs, I'd be glad to receive notice of it; you may contact at me the
supplied email-address.

=head1 COPYRIGHT

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

=head1 AUTHOR

Steven Schubiger, <steven@accognoscere.org>

=cut