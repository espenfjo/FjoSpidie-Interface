package FjoSpidie::SpiderManager;

use Moose;
use namespace::autoclean;
with qw(MooseX::Workers);

has 'spider' => (
    is  => 'rw',
    isa => 'Str',
);

sub run {
    my ( $self, $url ) = @_;

    my $runPath = $self->spawn( $self->spider );
    warn "Running now ... ";

    #    POE::Kernel->run();
}

# Implement our Interface
sub worker_stdout {
    shift;
    warn join ' ', @_;
}

sub worker_stderr {
    shift;
    warn join ' ', @_;
}

sub worker_manager_start {
    warn 'started worker manager';
}

sub worker_manager_stop {
    warn 'stopped worker manager';
}

sub max_workers_reached {
    warn 'maximum worker count reached';
}

sub worker_error {
    shift;
    warn join ' ', @_;
}

sub worker_done {
    shift;
    warn join ' ', @_;
}

sub worker_started {
    shift;
    warn join ' ', @_;
}

sub sig_child {
    shift;
    warn join ' ', @_;
}

sub sig_TERM {
    shift;
    warn 'Handled TERM';
}

__PACKAGE__->meta->make_immutable;

1;
__END__

=head1 NAME

FjoSpidie::SpiderManager - Perl extension for blah blah blah

=head1 SYNOPSIS

   use FjoSpidie::SpiderManager;
   blah blah blah

=head1 DESCRIPTION

Stub documentation for FjoSpidie::SpiderManager, 

Blah blah blah.

=head2 EXPORT

None by default.

=head1 SEE ALSO

Mention other useful documentation such as the documentation of
related modules or operating system documentation (such as man pages
in UNIX), or any relevant external documentation such as RFCs or
standards.

If you have a mailing list set up for your module, mention it here.

If you have a web site set up for your module, mention it here.

=head1 AUTHOR

Espen Fjellvær Olsen, E<lt>espen@mrfjo.orgE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2013 by Espen Fjellvær Olsen

This program is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.2 or,
at your option, any later version of Perl 5 you may have available.

=head1 BUGS

None reported... yet.

=cut
