package FjoSpidie::Controller::Report::Pcap;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller'; }

=head1 NAME

FjoSpidie::Controller::Pcap - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 download

=cut

sub pcap : Path : Args(1) {
    my ( $self, $c, $uuid ) = @_;

    my $res =
      $c->model('DB::Pcap')
      ->search( { 'report.uuid' => $uuid }, { join => 'report' } )->single();

    my $pcap = $res->data;
    $c->res->content_type('application/octet-stream');
    $c->res->body($pcap);
}

=head1 AUTHOR

  Espen Fjellvær Olsen

=head1 LICENSE

  This library is free software. You can redistribute it and/or modify
  it under the same terms as Perl itself.

=cut

__PACKAGE__->meta->make_immutable;

1;
