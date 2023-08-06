
vlccast = angular.module('vlccast', ['ngRoute', 'ngMaterial']);
MAX_VIDEOS = 50;

vlccast.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $routeProvider.when('/youtube', {
        templateUrl: '/static/views/youtube/index.html',
        controller: 'YoutubeController',
    });

    $routeProvider.when('/youtube/playlist/:playlist', {
        templateUrl: '/static/views/youtube/list.html',
        controller: 'YoutubePlaylistController',
    });

    $routeProvider.when('/youtube/video/:video', {
        templateUrl: '/static/views/player.html',
        controller: 'YoutubeVideoController',
    })

    $routeProvider.when('/googleauth', {
        templateUrl: '/static/views/googleauth.html',
        controller: 'GoogleAuthController',
    });

    $routeProvider.otherwise({
        redirectTo: '/youtube',
    });

    $locationProvider.html5Mode(true);
}]);

vlccast.filter('rate', function () {
    return function (input) {
        return input.toFixed(2) + 'x';
    };
});

vlccast.filter('seconds', function () {
    return function (input) {
        if (!input && input !== 0) {
            return '';
        }
        val = '';
        if (input >= 3600) {
            val += Math.floor(input/3600).toString();
            input = input%3600;
        } else {
            val += '0';
        }
        val += ':';
        if (input >= 60) {
            minutes = Math.floor(input/60).toString();
            input = input%60;
            if (minutes.length == 1) {
                val += '0';
            }
            val += minutes;
        } else {
            val += '00';
        }
        val += ':';
        seconds = input.toString();
        if (seconds.length == 1) {
            val += '0';
        }
        val += seconds;
        return val;
    };
});

vlccast.filter('duration', function () {
    var iso8601DurationRegex = /(-)?P(?:([\.,\d]+)Y)?(?:([\.,\d]+)M)?(?:([\.,\d]+)W)?(?:([\.,\d]+)D)?T(?:([\.,\d]+)H)?(?:([\.,\d]+)M)?(?:([\.,\d]+)S)?/;

    return function (input) {
        if (!input) {
            return '';
        }
        var matches = input.match(iso8601DurationRegex);
        str = '';
        if (matches[2]) {
            str += matches[2] + ' years ';
        }
        if (matches[3]) {
            str += matches[3] + ' months ';
        }
        if (matches[4]) {
            str += matches[4] + ' weeks ';
        }
        if (matches[5]) {
            str += matches[5] + ' days ';
        }
        if (matches[6]) {
            str += matches[6] + ':';
        }
        if (matches[7]) {
            if (matches[7].length == 1) {
                str += '0';
            }
            str += matches[7] + ':';
        } else {
            str += '00:'
        }
        if (matches[8]) {
            if (matches[8].length == 1) {
                str += '0';
            }
            str += matches[8];
        } else {
            str += '00';
        }
        return str;
    };
});

vlccast.controller('YoutubeController', ['$scope', 'youtubeService', function ($scope, youtubeService) {
    $scope.playlists = [];
    $scope.relatedPlaylists;
    youtubeService.playlistsListMy().then(function (response) {
        $scope.playlists = response.items;
    }, function (error) {
        console.log(error);
    });
    youtubeService.channelsListMy('contentDetails').then(function (response) {
        $scope.relatedPlaylists = response.items[0].contentDetails.relatedPlaylists;
    }, function (error) {
        console.log(error);
    });
}]);

vlccast.controller('YoutubeVideoController', ['$scope', 'youtubeService', '$routeParams', '$window', 'playerService', '$interval', '$timeout', function ($scope, youtubeService, $routeParams, $window, playerService, $interval, $timeout) {
    $scope.rates = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.50, 2.75, 3.0];
    if (!localStorage.getItem('vlccast-rate')) {
        $scope.rate = 1;
    } else {
        $scope.rate = localStorage.getItem('vlccast-rate');
    }
    $scope.length = 0;
    $scope.time = 0;
    $scope.playing = false;
    $scope.ready = false;

    youtubeService.videosGet($routeParams.video).then(function (response) {
        var video = response.items[0];
        var title = video.snippet.title;
        $scope.full_title = title;
        if (title.length > 20) {
            title = title.substr(0, 19) + '...';
        }
        $scope.title = title;
        $scope.image = video.snippet.thumbnails.high.url;
        $scope.text = video.snippet.description;
    }, function (error) {
        console.log(error);
    });

    playerService.play($routeParams.video).then(function (response) {
        $scope.volume = response.data.volume;
        $scope.length = response.data.length;
        if ($scope.rate != 1) {
            $scope.setRate();
        }
        $scope.ready = true;
        $scope.playing = true;
    });

    $scope.pause = function () {
        $scope.playing = !$scope.playing;
        playerService.pause();
    };

    $scope.seek = function () {
        playerService.seek($scope.time);
        $scope.progressactive = true;
        $timeout(function () {
            $scope.progressactive = false;
        });
    };

    $scope.setVolume = function () {
        playerService.volume($scope.volume);
        $scope.volumeactive = true;
        $timeout(function () {
            $scope.volumeactive = false;
        });
    };

    $scope.setRate = function () {
        playerService.rate($scope.rate);
        localStorage.setItem('vlccast-rate', $scope.rate);
    };

    var statusUpdate = $interval(function () {
        playerService.status().then(function (response) {
            if ($scope.playing && !response.data.playing) {
                $scope.playing = false;
            }
            $scope.time = response.data.time;
        });
    }, 1000);

    $scope.back = function () {
        $window.history.back();
    };

    $scope.$on('$destroy', function () {
        $interval.cancel(statusUpdate);
        playerService.stop();
    });
}]);

vlccast.controller('YoutubePlaylistController', ['$scope', 'youtubeService', '$routeParams', function ($scope, youtubeService, $routeParams) {
    var videoPlaylistItemIdsMap = {};
    $scope.videos = {
        _length: 0,
        _pages: {},
        _nextPageTokens: {},
        getItemAtIndex: function (index) {
            var pageNumber = Math.floor(index / MAX_VIDEOS);
            var page = this._pages[pageNumber];
            if (page) {
                return page[index % MAX_VIDEOS];
            } else if (page !== null) {
                this._loadPage(pageNumber);
            }
        },
        getLength: function () {
            return this._length;
        },
        _loadPage: function (pageNumber) {
            this._pages[pageNumber] = null;

            var pageToken;
            if (pageNumber != 0) {
                var nextPageToken = this._nextPageTokens[pageNumber-1];
                if (nextPageToken) {
                    pageToken = nextPageToken;
                } else {
                    return;
                }
            }

            youtubeService.playlistItemsList($routeParams.playlist, pageToken).then(angular.bind(this, function (response) {
                var ids = [];
                angular.forEach(response.items, function(playlistItem) {
                    ids.push(playlistItem.snippet.resourceId.videoId);
                    videoPlaylistItemIdsMap[playlistItem.snippet.resourceId.videoId] = playlistItem.id;
                });
                youtubeService.videosListById(ids, 'snippet,contentDetails').then(angular.bind(this, function (response) {
                    this._pages[pageNumber] = response.items;
                }), function (error) {
                    console.log(error);
                });
                this._nextPageTokens[pageNumber] = response.nextPageToken;
            }), function (error) {
                console.log(error);
            });
        },
    };
    youtubeService.playlistsGet($routeParams.playlist, 'snippet,contentDetails').then(function (response) {
        var playlist = response.items[0];
        $scope.title = playlist.snippet.title;
        $scope.videos._length = playlist.contentDetails.itemCount;
    }, function (error) {
        console.log(error);
    });
    $scope.remove = function (video) {
        youtubeService.playlistRemove(videoPlaylistItemIdsMap[video.id]).then(function () {
            $scope.videos._length -= 1;
            $scope.videos._pages = {};
            $scope.videos._nextPageTokens = {};
        });
    };
}]);

vlccast.controller('GoogleAuthController', ['$scope', 'googleApi', function ($scope, googleApi) {
    $scope.authorize = googleApi.authorize;
}]);

function googleApiClientReady () {
    window.initGapi();
}

vlccast.service('googleApi', ['$q', '$window', '$location', '$rootScope', function ($q, $window, $location, $rootScope) {
    var deferred = $q.defer();
    var OAUTH2_CLIENT_ID = '1012703545383-lba1jaantig270js44vnlvmf1dc7nb76.apps.googleusercontent.com';
    var OAUTH2_SCOPES = ['https://www.googleapis.com/auth/youtube'];

    $window.initGapi = function () {
        gapi.auth.init(function () {
            window.setTimeout(checkAuth, 1);
        });
    };

    var checkAuth = function () {
        gapi.auth.authorize({
            client_id: OAUTH2_CLIENT_ID,
            scope: OAUTH2_SCOPES,
            immediate: true,
        }, handleAuthResult);
    };

    var handleAuthResult = function (authResult) {
        if (authResult && !authResult.error) {
            gapi.client.load('youtube', 'v3', function() {
                if ($location.path() == '/googleauth') {
                    $window.history.back();
                }
                deferred.resolve(gapi);
            });
        } else {
            if (authResult.error == 'immediate_failed') {
                $rootScope.$apply(function () {
                    $location.path('/googleauth');
                });
            } else {
                deferred.reject(authResult.error);
            }
        }
    };

    this.get = function () {
        return deferred.promise;
    };

    this.authorize = function () {
        gapi.auth.authorize({
            client_id: OAUTH2_CLIENT_ID,
            scope: OAUTH2_SCOPES,
            immediate: false,
        }, handleAuthResult);
    };

}]);

vlccast.service('youtubeService', ['googleApi', '$q', function (googleApi, $q) {
    var MAX_PLAYLISTS = 50;

    this.playlistItemsList = function (playlist, pageToken='', part='snippet') {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.playlistItems.list({
                part: part,
                playlistId: playlist,
                maxResults: MAX_VIDEOS,
                pageToken: pageToken,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    };

    this.playlistsGet = function (id, part='snippet') {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.playlists.list({
                part: part,
                id: id,
                maxResults: 1,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    };

    this.playlistRemove = function (playlistItemId) {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.playlistItems.delete({
                id: playlistItemId,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    }

    this.playlistsListMy = function (part='snippet') {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.playlists.list({
                part: part,
                mine: true,
                maxResults: MAX_PLAYLISTS,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    };

    this.channelsListMy = function (part='snippet') {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.channels.list({
                part: part,
                mine: true,
                maxResults: 1,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    };


    this.videosGet = function (id, part='snippet') {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.videos.list({
                part: part,
                id: id,
                maxResults: 1,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    };

    this.videosListById = function (ids, part='snippet') {
        var deferred = $q.defer();

        googleApi.get().then(function (gapi) {
            gapi.client.youtube.videos.list({
                part: part,
                id: ids.join(),
                maxResults: MAX_VIDEOS,
            }).execute(function (response) {
                deferred.resolve(response.result);
            });
        }, function (error) {
            deferred.reject(error);
        });

        return deferred.promise;
    };


}]);

vlccast.service('playerService', ['$http', function ($http) {
    this.play = function (video_id) {
        return $http.post('/api/player/play', {video_id: video_id});
    };

    this.pause = function () {
        return $http.post('/api/player/pause');
    };

    this.stop = function () {
        return $http.post('/api/player/stop');
    };

    this.volume = function (volume) {
        return $http.post('/api/player/volume', {volume: volume});
    };

    this.rate = function (rate) {
        return $http.post('/api/player/rate', {rate: rate});
    };

    this.seek = function (time) {
        return $http.post('/api/player/seek', {time: time});
    };

    this.status = function() {
        return $http.get('/api/player/status');
    };
}]);
