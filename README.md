bangumi-alfred-workflow
====================

This workflow implements searching entries on [Bangumi](https://bgm.tv/)

Usage
--------------------

To search for entries,
```
bgm search QUERY
```

To log into an account,
```
bgm login EMAIL PASSWORD
```

To log out,
```
bgm login logout
```

To list all anime current watching,
```
bgm anime [QUERY]
```
and press `Enter` alone to open the url in browser, or `Cmd + Enter` to mark the next episode as watched.

Todo
--------------------

- [ ] Show icons when searching
- [x] Implement login feature
- [x] Implement features like marking episodes as watched

Used Resources
--------------------

`icon.png` is from [Bangumi](http://bgm.tv/img/ico/ico_ios.png)

`workflow` is the library [alfred-workflow](https://github.com/deanishe/alfred-workflow)

APIs are from [jabbany/dhufufu](https://github.com/jabbany/dhufufu/blob/master/bangumi/api.txt)
