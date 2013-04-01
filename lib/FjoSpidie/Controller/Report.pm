package FjoSpidie::Controller::Report;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller'; }

=head1 NAME

FjoSpidie::Controller::Report - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 report

=cut

sub report : Path : Args(1) {
    my ( $self, $c, $uuid ) = @_;

    my $report = $c->model('DB::Report')->search( { uuid => $uuid } )->single();

    my @alerts = $self->alerts( $c, $uuid );
    my @downloads = $self->downloads( $c, $uuid );
    my @connections = $self->headers( $c, $uuid );
    $c->stash(
        alerts      => @alerts,
        report_id   => $uuid,
        connections => \@connections,
        downloads   => @downloads,
        report      => $report,
    );

}

sub alerts {
    my ( $self, $c, $uuid ) = @_;
    return [ $c->model('DB::Alert')
          ->search( { "report.uuid" => $uuid }, { join => 'report', } ) ];
}

sub headers {
    my ( $self, $c, $uuid ) = @_;

    my @headers;

    my @entries =
      $c->model('DB::Entry')
      ->search( { "report.uuid" => $uuid }, { join => 'report', } );
    foreach my $entry (@entries) {
        my $entryId = $entry->id;

        my @requests = [
            $c->model('DB::Header')->search(
                {
                    type       => 'request',
                    'entry.id' => $entryId
                },
                { join => 'entry' },
            )
        ];
        my @responses = [
            $c->model('DB::Header')->search(
                {
                    type       => 'response',
                    'entry.id' => $entryId
                },
                { join => 'entry' },
            )
        ];

        my $request =
          $c->model('DB::Request')
          ->search( { 'entry.id' => $entryId }, { join => 'entry' } )->single();

        my $response =
          $c->model('DB::Response')
          ->search( { 'entry.id' => $entryId }, { join => 'entry' } )->single();

        my $data = {
            request   => $request,
            requests  => @requests,
            response  => $response,
            responses => @responses,
        };
        push( @headers, $data );
    }

    return @headers;
}

sub downloads {
    my ( $self, $c, $uuid ) = @_;
    return [ $c->model('DB::Download')
          ->search( { "report.uuid" => $uuid, }, { join => 'report' } ) ];
}

=head1 AUTHOR

Espen Fjellvær Olsen,,,

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

__PACKAGE__->meta->make_immutable;

1;
