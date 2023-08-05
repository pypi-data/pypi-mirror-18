'use strict';

angular.module('ajenti.plugins', ['core']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/plugins', {
        templateUrl: '/plugins:resources/partial/index.html',
        controller: 'PluginsIndexController'
    });
});

angular.module('ajenti.plugins').controller('PluginsIndexController', function ($scope, $q, $http, notify, pageTitle, messagebox, tasks, core, gettext) {
    pageTitle.set('Plugins');

    $scope.officialKeyFingerprint = '425E 018E 2394 4B4B 4281  4EE0 BDC3 FBAA 5302 9759';
    $scope.selectedInstalledPlugin = null;
    $scope.selectedRepoPlugin = null;
    $scope.coreUpgradeAvailable = null;

    $scope.selectRepoPlugin = function (plugin) {
        return $scope.selectedRepoPlugin = plugin;
    };

    $scope.refresh = function () {
        $http.get('/api/plugins/list/installed').success(function (data) {
            $scope.installedPlugins = data;
            $scope.repoList = null;
            $scope.repoListOfficial = null;
            $scope.repoListCommunity = null;
            $http.get('/api/plugins/repo/list').success(function (data) {
                $scope.repoList = data;
                $scope.notInstalledRepoList = $scope.repoList.filter(function (x) {
                    return !$scope.isInstalled(x);
                }).map(function (x) {
                    return x;
                });
                $scope.repoListOfficial = $scope.repoList.filter(function (x) {
                    return x.signature === $scope.officialKeyFingerprint;
                }).map(function (x) {
                    return x;
                });
                $scope.repoListCommunity = $scope.repoList.filter(function (x) {
                    return x.signature !== $scope.officialKeyFingerprint;
                }).map(function (x) {
                    return x;
                });
            }, function (err) {
                notify.error(gettext('Could not load plugin repository'), err.message);
            });
        }, function (err) {
            notify.error(gettext('Could not load the installed plugin list'), err.message);
        });

        $http.get('/api/plugins/core/check-upgrade').success(function (data) {
            return $scope.coreUpgradeAvailable = data;
        });

        $scope.pypiList = null;
        $http.get('/api/plugins/pypi/list').success(function (data) {
            return $scope.pypiList = data;
        });
    };

    $scope.refresh();

    $scope.isInstalled = function (plugin) {
        if (!$scope.isInstalled) {
            return false;
        }
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = $scope.installedPlugins[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                var p = _step.value;

                if (p.name === plugin.name) {
                    return true;
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

        return false;
    };

    $scope.isUninstallable = function (plugin) {
        return $scope.pypiList && $scope.pypiList[plugin.name] && plugin.name !== 'core';
    };

    $scope.isAnythingUpgradeable = function () {
        if (!$scope.installedPlugins) {
            return false;
        }
        if ($scope.coreUpgradeAvailable) {
            return true;
        }
        var _iteratorNormalCompletion2 = true;
        var _didIteratorError2 = false;
        var _iteratorError2 = undefined;

        try {
            for (var _iterator2 = $scope.installedPlugins[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                var p = _step2.value;

                if ($scope.getUpgrade(p)) {
                    return true;
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

        return false;
    };

    $scope.upgradeEverything = function () {
        return tasks.start('aj.plugins.plugins.tasks.UpgradeAll', [], {}).then(function (data) {
            return data.promise;
        }).then(function () {
            notify.success(gettext('All plugins updated'));
            messagebox.show({
                title: gettext('Done'),
                text: gettext('Installed. A panel restart is required.'),
                positive: gettext('Restart now'),
                negative: gettext('Later')
            }).then(function () {
                return core.forceRestart();
            });
        }).catch(function () {
            notify.error(gettext('Some plugins failed to update'));
        });
    };

    $scope.getUpgrade = function (plugin) {
        if (!$scope.repoList || !plugin) {
            return null;
        }
        var _iteratorNormalCompletion3 = true;
        var _didIteratorError3 = false;
        var _iteratorError3 = undefined;

        try {
            for (var _iterator3 = $scope.repoList[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                var p = _step3.value;

                if (p.name === plugin.name && p.version !== plugin.version) {
                    return p;
                }
            }
        } catch (err) {
            _didIteratorError3 = true;
            _iteratorError3 = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion3 && _iterator3.return) {
                    _iterator3.return();
                }
            } finally {
                if (_didIteratorError3) {
                    throw _iteratorError3;
                }
            }
        }

        return null;
    };

    $scope.installPlugin = function (plugin) {
        $scope.selectedRepoPlugin = null;
        $scope.selectedInstalledPlugin = null;
        var msg = messagebox.show({ progress: true, title: 'Installing' });
        return tasks.start('aj.plugins.plugins.tasks.InstallPlugin', [], { name: plugin.name, version: plugin.version }).then(function (data) {
            data.promise.then(function () {
                $scope.refresh();
                messagebox.show({ title: gettext('Done'), text: gettext('Installed. A panel restart is required.'), positive: gettext('Restart now'), negative: gettext('Later') }).then(function () {
                    return core.forceRestart();
                });
                return null;
            }, function (e) {
                notify.error(gettext('Install failed'), e.error);
            }).finally(function () {
                return msg.close();
            });
        });
    };

    $scope.uninstallPlugin = function (plugin) {
        if (plugin.name === 'plugins') {
            return messagebox.show({
                title: gettext('Warning'),
                text: gettext('This will remove the Plugins plugin. You can reinstall it later using PIP.'),
                positive: gettext('Continue'),
                negative: gettext('Cancel')
            }).then(function () {
                return $scope.doUninstallPlugin(plugin);
            });
        } else {
            return $scope.doUninstallPlugin(plugin);
        }
    };

    $scope.doUninstallPlugin = function (plugin) {
        $scope.selectedRepoPlugin = null;
        $scope.selectedInstalledPlugin = null;
        return messagebox.show({
            title: gettext('Uninstall'),
            text: gettext('Uninstall ' + plugin.name + '?'),
            positive: gettext('Uninstall'),
            negative: gettext('Cancel')
        }).then(function () {
            var msg = messagebox.show({ progress: true, title: gettext('Uninstalling') });
            return $http.get('/api/plugins/pypi/uninstall/' + plugin.name).success(function () {
                $scope.refresh();
                return messagebox.show({
                    title: gettext('Done'),
                    text: gettext('Uninstalled. A panel restart is required.'),
                    positive: gettext('Restart now'),
                    negative: gettext('Later')
                }).then(function () {
                    core.forceRestart();
                });
            }, function (err) {
                notify.error(gettext('Uninstall failed'), err.message);
            }).finally(function () {
                msg.close();
            });
        });
    };

    $scope.restart = function () {
        return core.restart();
    };
});


