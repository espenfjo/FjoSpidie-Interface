package FjoSpidie::Controller::Reports;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller'; }

=head1 NAME

FjoSpidie::Controller::Reports - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 reports

=cut

sub reports : Path : Args(0) {
    my ( $self, $c ) = @_;

    $c->stash(
        reports => [
            $c->model('DB::Report')
              ->search( { endtime => { '!=', "0000-00-00 00:00:00" } } )
        ]
    );
}

=head1 AUTHOR

Espen Fjellvær Olsen,,,

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

__PACKAGE__->meta->make_immutable;

1;
