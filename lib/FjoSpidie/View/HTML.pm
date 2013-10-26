package FjoSpidie::View::HTML;
use Moose;
use namespace::autoclean;

extends 'Catalyst::View::TT';

__PACKAGE__->config(
    TEMPLATE_EXTENSION => '.tt2',
    render_die         => 1,
    TIMER              => 1,
    DEBUG              => 'all',

    # This is your wrapper template located in the 'root/src'
    WRAPPER => 'layouts/layout.tt2',
);

=head1 NAME

FjoSpidie::View::HTML - TT View for FjoSpidie

=head1 DESCRIPTION

TT View for FjoSpidie.

=head1 SEE ALSO

L<FjoSpidie>

=head1 AUTHOR

Espen Fjellvær Olsen,,,

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

1;
