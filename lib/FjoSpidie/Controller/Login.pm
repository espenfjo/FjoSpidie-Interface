package FjoSpidie::Controller::Login;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller'; }

=head1 NAME

FjoSpidie::Controller::Login - Catalyst Controller

=head1 DESCRIPTION

Catalyst Controller.

=head1 METHODS

=cut

=head2 index

=cut

sub login : Path : Args(0) {
    my ( $self, $c ) = @_;

    my $error;

    # Get the username and password from form
    my $username = $c->request->params->{username};
    my $password = $c->request->params->{password};
    if ( $username && $password ) {

        # Attempt to log the user in
        if (
            $c->authenticate(
                {
                    username => $username,
                    password => $password

                }
            )
          )
        {
            # If successful, then let them use the application
            $c->response->redirect(
                $c->uri_for( $c->controller('Reports')->action_for('reports') )
            );
            return;
        }
        else {
            # Set an error message
            $error = "Bad username or password.";
        }
    }

    else {
        # Set an error message
        $error = "Empty username or password." unless ( $c->user_exists );

    }

    # If either of above don't work out, send to the login page
    #    $c->response->redirect( $c->uri_for( $c->controller('Root') ) );

    $c->flash( message => "Welcome to the FjoSpidie honey spider!" );

#    $c->response->redirect({mid => $c->set_error_msg("Error deleting widget")}));

    $c->response->redirect(
        $c->uri_for( '/', { mid => $c->set_error_msg($error) } ) );

}

=head1 AUTHOR

Espen Fjellvær Olsen,,,

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

__PACKAGE__->meta->make_immutable;

1;
