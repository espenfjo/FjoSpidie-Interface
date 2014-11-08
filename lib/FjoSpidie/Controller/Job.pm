package FjoSpidie::Controller::Job;
use Moose;
use namespace::autoclean;
use Data::UUID;
use English qw(-no_match_vars);

BEGIN { extends 'Catalyst::Controller::REST'; }

=head1 NAME

FjoSpidie::Controller::Job - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 index

=cut

__PACKAGE__->config( default => 'application/json', );

sub job : Path('') : ActionClass('REST') {
}

sub job_GET {
    my ( $self, $c, $uuid ) = @_;

    my $report = $c->model('DB::Report')->find( { uuid => $uuid } );
    if ($report) {
        if ( $report->endtime =~ /0000-00-00 00:00:00/
            || !defined $report->endtime )
        {
            $self->status_found( $c, entity => {} );
        }
        else {
            $self->status_ok( $c, entity => { $uuid, "ok" } );
        }

    }
    else {
        $self->status_not_found( $c, message => "$uuid not found" );
    }

}

sub job_POST {
    my ( $self, $c ) = @_;
    my ( $url, $referer, $ua );
    use Data::Dumper;

    $c->log->debug( Dumper( $c->req->data ) );
    $c->log->debug( Dumper( $c->request->params ) );

    eval {
        $url = $c->request->params->{url};
        $url ||= $c->req->data->{url};

        $referer = $c->request->params->{ref};
        $referer ||= $c->req->data->{ref};

        $ua = $c->request->params->{useragent};
        $ua ||= $c->req->data->{useragent};

        1;
    };

    my $command = $c->config->{fjospidie_runsh};
    my $ug      = Data::UUID->new();
    my $uuid    = lc( $ug->create_str() );
    $c->log->debug( "URL " . $url . " REF: " . $referer . " UA: " . $ua );

    $self->run( $c, $command, $url, $referer, $ua, $uuid );

    $self->status_created(
        $c,
        location => $c->req->uri->as_string,
        entity   => {
            url  => $url,
            uuid => $uuid
        }
    );

}

sub run {
    my $self    = shift;
    my $c       = shift;
    my $command = shift;
    my $url     = shift;
    my $referer = shift;
    my $ua      = shift;
    my $uuid    = shift;

    my @command = ( $command, "--url", "'$url'", "--uuid", $uuid );
    if ($referer) {
        push( @command, "--referer" );
        push( @command, "\\\"'$referer'\\\"" );
    }
    if ($ua) {
        push( @command, "--useragent" );
        push( @command, "\\\"'$ua'\\\"" );
    }
    eval {
        local $SIG{ALRM} = sub { die "timeout\n" };
        alarm(300);
        $c->log->debug( "Starting FjoSpidie: " . join( " ", @command ) );

        my $pid = fork();
        die "cannot fork: $ERRNO\n" unless defined $pid;
        if ( $pid == 0 ) {
            exec( { $command[0] } @command );
        }
        else {
            #    waitpid( $pid, 0 );
        }

        undef $pid;
        1;
    } or do {
        alarm(0);
        if ( $EVAL_ERROR eq "timeout\n" ) {
            $c->log->info("FjoSpidie experienced an timeout on $url");
        }
        elsif ( $EVAL_ERROR =~ /^cannot fork/ ) {
            $c->log->info("FjoSpidie cannot fork $ERRNO $EVAL_ERROR");
        }
        else {
            $c->log->info("FjoSpidie cannot fork $ERRNO $EVAL_ERROR");
        }
    };

}

=head1 AUTHOR

Espen Fjellvær Olsen,,,

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

__PACKAGE__->meta->make_immutable;

1;
