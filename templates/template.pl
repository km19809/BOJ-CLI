#!/usr/bin/perl
# BOJ 1000 Perl
# 출처: https://www.acmicpc.net/help/language 
my $a = <STDIN>;
my @b = split(/ /, $a);

my $ans = @b[0] + @b[1];

print $ans;