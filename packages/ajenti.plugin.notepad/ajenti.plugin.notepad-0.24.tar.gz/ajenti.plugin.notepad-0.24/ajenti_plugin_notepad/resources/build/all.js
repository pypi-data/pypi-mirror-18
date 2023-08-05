'use strict';

angular.module('ajenti.notepad', ['core', 'ajenti.filesystem', 'ajenti.ace']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/notepad', {
        templateUrl: '/notepad:resources/partial/index.html',
        controller: 'NotepadIndexController'
    });

    $routeProvider.when('/view/notepad/:path*', {
        templateUrl: '/notepad:resources/partial/index.html',
        controller: 'NotepadIndexController'
    });
});


'use strict';

angular.module('ajenti.notepad').controller('NotepadIndexController', function ($scope, $routeParams, $location, notify, filesystem, pageTitle, hotkeys, config, gettext) {
    pageTitle.set('');

    $scope.newFile = function () {
        if ($scope.content) {
            if (!confirm(gettext('Current file will be closed. Continue?'))) {
                return;
            }
        }
        $scope.path = null;
        $scope.content = '';
    };

    $scope.showOpenDialog = function () {
        return $scope.openDialogVisible = true;
    };

    $scope.open = function (path) {
        var url = '/view/notepad/' + path;
        if ($location.path() !== url) {
            $location.path(url);
            return;
        }

        $scope.openDialogVisible = false;
        $scope.path = path;
        pageTitle.set(path);

        return filesystem.read($scope.path).then(function (content) {
            $scope.content = content;
            $scope.$broadcast('ace:reload', $scope.path);
        }, function (err) {
            notify.error(gettext('Could not open the file'), err.message);
        });
    };

    $scope.save = function () {
        return $scope.saveAs($scope.path);
    };

    $scope.saveAs = function (path) {
        $scope.saveDialogVisible = false;
        var mustReload = path !== $scope.path;
        $scope.path = path;
        return filesystem.write($scope.path, $scope.content).then(function () {
            notify.success('Saved', $scope.path);
            if (mustReload) {
                return $scope.open($scope.path);
            } else {
                $scope.$broadcast('ace:reload', $scope.path);
            }
        }, function (err) {
            notify.error(gettext('Could not save the file'), err.message);
        });
    };

    $scope.showSaveDialog = function () {
        $scope.saveDialogVisible = true;
        if ($scope.path) {
            var t = $scope.path.split('/');
            $scope.saveAsName = t[t.length - 1];
        } else {
            $scope.saveAsName = 'new.txt';
        }
    };

    config.getUserConfig().then(function (userConfig) {
        $scope.userConfig = userConfig;
        $scope.userConfig.notepad = $scope.userConfig.notepad || {};
        $scope.userConfig.notepad.bookmarks = $scope.userConfig.notepad.bookmarks || [];
        $scope.bookmarks = $scope.userConfig.notepad.bookmarks;
    });

    $scope.toggleBookmark = function () {
        $scope.bookmarks.toggleItem($scope.path);
        config.setUserConfig($scope.userConfig);
    };

    if ($routeParams.path) {
        $scope.open($routeParams.path);
    } else {
        $scope.newFile();
    }

    hotkeys.on($scope, function (key, event) {
        if (key === 'O' && event.ctrlKey) {
            $scope.showOpenDialog();
            return true;
        }
        if (key === 'S' && event.ctrlKey) {
            if ($scope.path && !event.shiftKey) {
                $scope.save();
            } else {
                $scope.showSaveDialog();
            }
            return true;
        }
        if (key === 'N' && event.ctrlKey) {
            $scope.newFile();
            return true;
        }
        return false;
    });
});


