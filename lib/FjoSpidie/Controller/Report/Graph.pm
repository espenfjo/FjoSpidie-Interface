package FjoSpidie::Controller::Graph;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller'; }

=head1 NAME

FjoSpidie::Controller::Report - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 graph

=cut

sub graph : Path('/report/graph') : Args(1) {
    my ( $self, $c, $uuid ) = @_;

    my $res =
      $c->model('DB::Graph')
      ->search( { 'report.uuid' => $uuid }, { join => 'report' } )->single();

    my $img = $res->graph;
    $c->res->content_type('image/png');
    $c->res->body($img);
}
__PACKAGE__->meta->make_immutable;

1;
