'use strict';

angular.module('ajenti.filemanager', ['core', 'ajenti.filesystem']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/filemanager', {
        templateUrl: '/filemanager:resources/partial/index.html',
        controller: 'FileManagerIndexController'
    });

    $routeProvider.when('/view/filemanager/properties/:path*', {
        templateUrl: '/filemanager:resources/partial/properties.html',
        controller: 'FileManagerPropertiesController'
    });

    return $routeProvider.when('/view/filemanager/:path*', {
        templateUrl: '/filemanager:resources/partial/index.html',
        controller: 'FileManagerIndexController'
    });
});


'use strict';

angular.module('ajenti.filemanager').controller('FileManagerIndexController', function ($scope, $routeParams, $location, $localStorage, $timeout, notify, identity, filesystem, pageTitle, urlPrefix, tasks, messagebox, $upload, gettext) {
    pageTitle.set('path', $scope);
    $scope.loading = false;
    $scope.newDirectoryDialogVisible = false;
    $scope.newFileDialogVisible = false;
    $scope.clipboardVisible = false;

    $scope.load = function (path) {
        $scope.loading = true;
        return filesystem.list(path).then(function (data) {
            $scope.path = path;
            $scope.items = data.items;
            $scope.parent = data.parent;
        }, function (data) {
            notify.error(gettext('Could not load directory'), data.message);
        }).finally(function () {
            $scope.loading = false;
        });
    };

    $scope.refresh = function () {
        return $scope.load($scope.path);
    };

    $scope.$on('push:filesystem', function ($event, msg) {
        if (msg === 'refresh') {
            $scope.refresh();
        }
    });

    $scope.navigate = function (path) {
        return $location.path(urlPrefix + '/view/filemanager/' + path);
    };

    $scope.select = function (item) {
        if (item.isDir) {
            $scope.navigate(item.path);
        } else {
            if ($scope.mode === 'open') {
                $scope.onSelect({ item: item });
            }
            if ($scope.mode === 'save') {
                $scope.name = item.name;
            }
        }
    };

    $scope.clearSelection = function () {
        $scope.items.forEach(function (item) {
            return item.selected = false;
        });
    };

    $localStorage.fileManagerClipboard = $localStorage.fileManagerClipboard || [];
    $scope.clipboard = $localStorage.fileManagerClipboard;

    $scope.showClipboard = function () {
        return $scope.clipboardVisible = true;
    };

    $scope.hideClipboard = function () {
        return $scope.clipboardVisible = false;
    };

    $scope.clearClipboard = function () {
        $scope.clipboard.length = 0;
        $scope.hideClipboard();
    };

    $scope.doCut = function () {
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = $scope.items[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                var item = _step.value;

                if (item.selected) {
                    $scope.clipboard.push({
                        mode: 'move',
                        item: item
                    });
                }
            }
        } catch (err) {
            _didIteratorError = true;
            _iteratorError = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion && _iterator.return) {
                    _iterator.return();
                }
            } finally {
                if (_didIteratorError) {
                    throw _iteratorError;
                }
            }
        }

        $scope.clearSelection();
    };

    $scope.doCopy = function () {
        var _iteratorNormalCompletion2 = true;
        var _didIteratorError2 = false;
        var _iteratorError2 = undefined;

        try {
            for (var _iterator2 = $scope.items[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                var item = _step2.value;

                if (item.selected) {
                    $scope.clipboard.push({
                        mode: 'copy',
                        item: item
                    });
                }
            }
        } catch (err) {
            _didIteratorError2 = true;
            _iteratorError2 = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion2 && _iterator2.return) {
                    _iterator2.return();
                }
            } finally {
                if (_didIteratorError2) {
                    throw _iteratorError2;
                }
            }
        }

        $scope.clearSelection();
    };

    $scope.doDelete = function () {
        return messagebox.show({
            text: gettext('Delete selected items?'),
            positive: gettext('Delete'),
            negative: gettext('Cancel')
        }).then(function () {
            var items = $scope.items.filter(function (item) {
                return item.selected;
            });
            tasks.start('aj.plugins.filesystem.tasks.Delete', [], { items: items });
            $scope.clearSelection();
        });
    };

    $scope.doPaste = function () {
        var items = angular.copy($scope.clipboard);
        tasks.start('aj.plugins.filesystem.tasks.Transfer', [], { destination: $scope.path, items: items }).then(function () {
            $scope.clearClipboard();
        });
    };

    // new file dialog

    $scope.showNewFileDialog = function () {
        $scope.newFileName = '';
        $scope.newFileDialogVisible = true;
    };

    $scope.doCreateFile = function () {
        if (!$scope.newFileName) {
            return;
        }

        return filesystem.createFile($scope.path + '/' + $scope.newFileName).then(function () {
            $scope.refresh();
            $scope.newFileDialogVisible = false;
        }, function (err) {
            notify.error(gettext('Could not create file'), err.message);
        });
    };

    // new directory dialog

    $scope.showNewDirectoryDialog = function () {
        $scope.newDirectoryName = '';
        $scope.newDirectoryDialogVisible = true;
    };

    $scope.doCreateDirectory = function () {
        if (!$scope.newDirectoryName) {
            return;
        }

        return filesystem.createDirectory($scope.path + '/' + $scope.newDirectoryName).then(function () {
            $scope.refresh();
            $scope.newDirectoryDialogVisible = false;
        }, function (err) {
            notify.error(gettext('Could not create directory'), err.message);
        });
    };

    // upload dialog
    $scope.uploadFiles = [];
    $scope.uploadPending = [];

    $scope.showUploadDialog = function () {
        return $scope.uploadDialogVisible = true;
    };

    var uploadCallback = function uploadCallback() {
        if ($scope.uploadPending.length > 0) {
            $scope.uploadCurrent = {
                file: $scope.uploadPending[0],
                name: $scope.uploadPending[0].name
            };
            $scope.uploadPending.remove($scope.uploadCurrent.file);
            $upload.upload({
                url: urlPrefix + '/api/filesystem/upload/' + $scope.path + '/' + $scope.uploadCurrent.name,
                file: $scope.uploadCurrent.file,
                fileName: $scope.uploadCurrent.name,
                fileFormDataName: 'upload'
            }).success(function () {
                notify.success(gettext('Uploaded'), $scope.uploadCurrent.name);
                $scope.refresh();
                return uploadCallback();
            }).xhr(function (xhr) {
                return $scope.uploadCurrent.cancel = function () {
                    return xhr.abort();
                };
            }).progress(function (e) {
                $scope.uploadCurrent.length = e.total;
                $scope.uploadCurrent.progress = e.loaded;
            }).error(function (e) {
                if ($scope.uploadCurrent) {
                    notify.error(gettext('Upload failed'), $scope.uploadCurrent.name);
                    uploadCallback();
                } else {
                    notify.info(gettext('Upload cancelled'));
                }
            });
        } else {
            $scope.uploadDialogVisible = false;
            $scope.uploadPending = [];
            $scope.uploadRunning = false;
            $scope.uploadCurrent = null;
        }
    };

    $scope.doUpload = function () {
        return $timeout(function () {
            $scope.uploadRunning = true;
            $scope.uploadPending = $scope.uploadFiles;
            $scope.uploadFiles = [];
            uploadCallback();
        });
    };

    $scope.cancelUpload = function () {
        $scope.uploadDialogVisible = false;
        $scope.uploadFiles = [];
        $scope.uploadPending = [];
        $scope.uploadRunning = false;
        if ($scope.uploadCurrent) {
            $scope.uploadCurrent.cancel();
            $scope.uploadCurrent = null;
        }
    };

    // ---

    identity.promise.then(function () {
        var root = identity.profile.fs_root || '/';
        var path = $routeParams.path || '/';
        if (path.indexOf(root) !== 0) {
            path = root;
        }

        if ($routeParams.path) {
            $scope.load(path);
        } else {
            $scope.navigate(root);
        }
    });
});


'use strict';

angular.module('ajenti.filemanager').controller('FileManagerPropertiesController', function ($scope, $routeParams, $location, notify, filesystem, pageTitle, urlPrefix, gettext) {
    pageTitle.set('path', $scope);

    var modeBits = ['ax', 'aw', 'ar', 'gx', 'gw', 'gr', 'ux', 'uw', 'ur', 'sticky', 'setuid', 'setgid'];
    $scope.permissionsDialogVisible = false;

    $scope.path = $routeParams.path;
    $scope.refresh = function () {
        return filesystem.stat($scope.path).then(function (info) {
            $scope.info = info;
            $scope.mode = {};
            for (var i = 0; i < modeBits.length; i++) {
                $scope.mode[modeBits[i]] = !!($scope.info.mode & Math.pow(2, i));
            }
        }, function (err) {
            notify.error(gettext('Could not read file information'), err);
        });
    };

    $scope.hidePermissionsDialog = function () {
        return $scope.permissionsDialogVisible = false;
    };

    $scope.applyPermissions = function () {
        $scope.hidePermissionsDialog();

        var mode = 0;
        for (var i = 0; i < modeBits.length; i++) {
            mode += $scope.mode[modeBits[i]] ? Math.pow(2, i) : 0;
        }

        return filesystem.chmod($scope.path, mode).then(function () {
            notify.info(gettext('File mode saved'));
            $scope.refresh();
        });
    };

    $scope.refresh();
});


