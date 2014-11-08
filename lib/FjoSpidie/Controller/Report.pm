package FjoSpidie::Controller::Report;
use Moose;
use Net::DNS;
use URI;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller::REST'; }

=head1 NAME

FjoSpidie::Controller::Report - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 report

=cut

__PACKAGE__->config( map => { 'text/html' => [ 'View', 'HTML' ], } );

sub report : Path : ActionClass('REST') {
    my ( $self, $c, $uuid ) = @_;

}

sub report_GET : Path : Args(1) {
    my ( $self, $c, $uuid ) = @_;

    if (   $c->request->headers->header('Content-Type')
        && $c->request->headers->header('Content-Type') eq 'application/json' )
    {

        $c->forward( 'job', 'job_GET' );
        return;
    }

    my $report = $c->model('DB::Report')->search( { uuid => $uuid } )->single();
    my @alerts = $self->alerts( $c, $uuid );
    my @downloads = $self->downloads( $c, $uuid );
    my @connections = $self->headers( $c, $uuid );
    my $pcap = $self->pcap( $c, $uuid );

    @connections = $self->findSuspiciousRequest($c, $report, @alerts, \@connections);


    if ($pcap) {
        $pcap->{length} = $pcap->get_column('data_length');
    }

    $c->stash(
        alerts      => @alerts,
        report_id   => $uuid,
        connections => \@connections,
        downloads   => @downloads,
        report      => $report,
        pcap        => $pcap,
    );
    $c->stash->{template} = 'report/report.tt2';
}

sub findSuspiciousRequest{
    my ( $self, $c, $report, $a, $co) = @_;
    my %checked;
    my @site_ip;
    my @alerts      =  @{$a};
    my @connections = @{ $co };

    return unless $report;
    my $res = Net::DNS::Resolver->new;
    my $uri = $report->url;
    my $url = URI->new( $uri );
    my $domain = $url->host;

    my $query = $res->search( $domain );
    if ($query) {
	foreach my $rr ($query->answer) {
	    next unless $rr->type eq "A";
	    my $ip = $rr->address;
	    push(@site_ip, $ip);
	}
    }

    
    foreach my $alert ( @alerts ) {
	while( my ($index, $connection) = each @connections ) {
	    my $host = $connection->{request}->{host};
	    my $query = $res->search($host);
	    
	    if ($query) {
		foreach my $rr ($query->answer) {
		    next unless $rr->type eq "A";
		    my $ip = $rr->address;
		    print STDERR "Checking if " . $ip . " equals to " . $alert->from_ip . " or " . $alert->to_ip ."\n";

		    if ( $alert->from_ip =~ /$ip/  || $alert->to_ip =~ /$ip/) {
			next if grep { /$ip/ } @site_ip;
			$connections[$index]->{suspicious} = 1;
		    }
		    $checked{ $host } = 1;
		}
	    } else {
		warn "query failed: ", $res->errorstring, "\n";
	    };
	    
	    
	}
	
    }
    return @connections;
}

sub alerts {
    my ( $self, $c, $uuid ) = @_;
    return [ $c->model('DB::Alert')
          ->search( { "report.uuid" => $uuid }, { join => 'report', } ) ];
}

sub headers {
    my ( $self, $c, $uuid ) = @_;
    my @entries =
      $c->model('DB::Entry')
      ->search( { "report.uuid" => $uuid }, { join => 'report', } );
    my @entryIDs = map { $_->id } @entries;

    my $headers = $c->model('DB')->storage->dbh_do(
        sub {
            my ( $storage, $dbh, $uuid ) = @_;
            my $statement =
"SELECT me.id, me.entry_id, me.name, me.value, me.type,  requests.host, requests.port, responses.httpversion, responses.statustext, responses.status, responses.bodysize, responses.headersize, requests.bodysize, requests.headersize, requests.method, requests.uri, requests.httpversion FROM header me  JOIN entry entry ON entry.id = me.entry_id  JOIN report report ON report.id = entry.report_id LEFT JOIN response responses ON responses.entry_id = entry.id LEFT JOIN request requests ON requests.entry_id = entry.id WHERE ( report.uuid = \'$uuid\' ) ORDER BY requests.id ASC";

            my $sth = $dbh->prepare($statement);
            $sth->execute();

            $sth->fetchall_hashref("id");
        },
        $uuid
    );
    my %data;
    foreach my $header ( values %$headers ) {
        push(
            @{ $data{ $header->{entry_id} }{ $header->{type} . 's' } },
            { name => $header->{name}, value => $header->{value} }
        );

        $data{ $header->{entry_id} }{response} = {
            id          => $header->{id},
            status      => $header->{status},
            statustext  => $header->{statustext},
            httpversion => $header->{httpversion}
        };

        $data{ $header->{entry_id} }{request} = {
            id          => $header->{id},
            host        => $header->{host},
            port        => $header->{port},
            method      => $header->{method},
            uri         => $header->{uri},
            httpversion => $header->{httpversion}
        };
    }

    my @vals;

    foreach ( sort keys %data ) {
        push @vals, $data{$_};
    }

    return (@vals);
}

sub downloads {
    my ( $self, $c, $uuid ) = @_;
    return [ $c->model('DB::Download')
          ->search( { "report.uuid" => $uuid, }, { join => 'report' } ) ];
}

sub pcap {
    my ( $self, $c, $uuid ) = @_;
    return $c->model('DB::Pcap')->search(
        { "report.uuid" => $uuid, },
        {
            join   => 'report',
            select => [ 'data', { LENGTH => 'data', -as => 'length' } ],
            as     => [qw/ data data_length /],
        },
    )->single();
}

=head1 AUTHOR

Espen Fjellvær Olsen,,,

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

__PACKAGE__->meta->make_immutable;

1;
