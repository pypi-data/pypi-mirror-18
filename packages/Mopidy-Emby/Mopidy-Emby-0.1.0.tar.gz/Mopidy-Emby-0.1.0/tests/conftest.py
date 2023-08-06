import mock

import pytest

import mopidy_emby


@pytest.fixture
def config():
    return {
        'emby': {
            'hostname': 'https://foo.bar',
            'port': 443,
            'username': 'embyuser',
            'password': 'embypassword'
        },
        'proxy': {
            'foo': 'bar'
        }
    }


@pytest.fixture
def emby_client(config, mocker):
    mocker.patch('mopidy_emby.backend.EmbyHandler._get_token')
    mocker.patch('mopidy_emby.backend.EmbyHandler._create_headers')
    mocker.patch('mopidy_emby.backend.EmbyHandler._get_user',
                 return_value=[{'Id': 'mock'}])
    mocker.patch('mopidy_emby.backend.EmbyHandler._password_data')

    return mopidy_emby.backend.EmbyHandler(config)


@pytest.fixture
def backend_mock():
    backend_mock = mock.Mock(autospec=mopidy_emby.backend.EmbyBackend)

    return backend_mock


@pytest.fixture
def libraryprovider(backend_mock):
    backend_mock.remote(autospec=mopidy_emby.backend.EmbyHandler)
    backend_mock.remote.get_artists.return_value = ['Artistlist']
    backend_mock.remote.get_albums.return_value = ['Albumlist']
    backend_mock.remote.get_tracks.return_value = ['Tracklist']
    backend_mock.remote.get_track.return_value = {
        'Name': 'Foo',
        'Id': 123
    }

    return mopidy_emby.backend.EmbyLibraryProvider(backend_mock)


@pytest.fixture
def playbackprovider(backend_mock, emby_client):
    backend_mock.remote = emby_client

    return mopidy_emby.backend.EmbyPlaybackProvider(audio=mock.Mock(),
                                                    backend=backend_mock)
