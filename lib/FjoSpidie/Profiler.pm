package FjoSpidie::Profiler;
use strict;
use Time::HiRes qw(time);
use base 'DBIx::Class::Storage::Statistics';
my $start;

sub query_start {
    my $self   = shift();
    my $sql    = shift();
    my @params = @_;

    $self->print( "Executing $sql: " . join( ', ', @params ) . "\n" );
    $start = time();
}

sub query_end {
    my $self   = shift();
    my $sql    = shift();
    my @params = @_;

    my $elapsed = sprintf( "%0.4f", time() - $start );
    $self->print("Execution took $elapsed seconds.\n");
    $start = undef;
}
1;

