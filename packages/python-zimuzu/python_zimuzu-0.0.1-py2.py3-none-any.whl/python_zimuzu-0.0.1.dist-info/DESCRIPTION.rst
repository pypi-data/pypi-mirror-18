字幕组网站(www.zimuzu.tv)接口,命令行工具及更新推送服务

Home-page: https://github.com/er1iang/python-zimuzu
Author: UNKNOWN
Author-email: UNKNOWN
License: GPLv3
Description: # python-zimuzu
        [![license](https://img.shields.io/github/license/er1iang/python-zimuzu.svg)](https://github.com/er1iang/python-zimuzu/blob/master/LICENSE)
        [![license](https://img.shields.io/pypi/v/python-zimuzu.svg)](https://pypi.python.org/pypi/python-zimuzu)
        [![license](https://img.shields.io/badge/Status-Developing-yellow.svg)](https://github.com/er1iang/python-zimuzu/)
        ---
        
        [字幕组网站](www.zimuzu.tv)接口,命令行工具及更新推送服务
        
        ```
        $ python zimuzu --help
        Usage: zimuzu [OPTIONS] COMMAND [ARGS]...
        
          字幕组网站(www.zimuzu.tv)接口
        
        Options:
          -c, --config FILENAME  配置文件路径
          --cid TEXT             cid
          --key TEXT             accesskey
          -v, --verbose          显示更多信息
          --help                 Show this message and exit.
        
        Commands:
          api     请求字幕组网站接口
          daemon  字幕组网站资源自动更新服务
        ```
        
        ## 特性/路线
        
        - [x] 提供了命令行调试接口
        - [x] 支持配置文件导入导出
        - [x] 支持插件
        - [x] 提供了字幕组网站资源自动更新服务
            - [x] 支持自定义更新间隔
            - [x] 支持更新资源过滤
                - [x] 字段正则过滤器
            - [x] 支持更新资源处理
                - [x] 终端输出处理器
                - [x] 邮件通知处理器
                - [ ] 自动下载处理器
                    - [ ] Transmission
                    - [ ] 小米路由器远程下载
        
        
        ## 文档
        ### 安装
        
        ```
        $pip install python-zimuzu
        ```
        
        待更新 ...
        
        ## FAQ
        
        - 为什么使用GPL协议?
            
            >字幕组由网络爱好者自发组成,不以盈利为目的,加入仅凭个人兴趣爱好,没有任何金钱实质回报
            
            我希望开发者同字幕组一样有分享与奉献精神.
            
           
        - 为什么没提供接口地址?
        
            避免被未知力量封杀:no_mouth:
            
        - 兼容性如何?
           
           保证 Python>=3.3 版本的兼容性, 不做向下兼容, 都什么年代了还用 Python2 ?
            
        
        
        ## 接口说明(update at: 2016-12-03)
        每个合作方都会分配一个唯一的验证码,在获取接口的时候需要传递合作方ID和验证码
        接口验证方式有以下两种
        
        1. 在传递的参数中包含合作方ID和分配的验证码,适用于通过服务器获取接口数据
        2. 在APP上使用的接口会验证链接是否有效,需要先加密再- 传递参数
        
        必要参数:
        
        - cid:接口ID
        - accesskey:加密后的参数(与未加密时使用的参数名一样)
        - timestamp:客户端发送请求时的UNIX时间戳(程序会验证该时间与服务器时间,如果超过5分钟就视为无效链接)
        - client:客户端类型,1-IOS 2-安卓 3-WP
        
        accesskey生成方法:`md5('cid$$accesskey&&timestamp')`
        
        变量说明:
        
        - cid:分配的接口ID
        - timestamp:客户端发送请求时的UNIX时间戳
        - accesskey:分配给接口的密钥
        
        数据目前可返回格式包含了json,jsonp,xml,调用方式为传递type参数,如`/resource/today?type=jsonp`
        
        poster字段说明:
        
        部分接口中除了返回poster字段外,还返回了poster_s,poster_m,poster_b,poster_a四个字段,分别是不同尺寸的海报链接地址
        
        season字段说明(仅针对电视剧类型,电影的season字段为0):
        
        - 0 前传
        - 101 单剧
        - 102  MINI剧
        - 103 周边资源
        - 1-100为正常的季度信息
        - 接口权限验证错误代码说明
        - 1001 传递的参数错误
        - 1002 请求链接验证失败
        - 1003  accesskey错误
        - 1004 接口未授权
        - 1011 请求链接验证失败
        - 1012 接口请求超时
        - 1021 未登录
        
        
        ### APP首页数据接口
        - 接口地址:/focus/index
        - 返回数据:
        
        ```
        focus_list 焦点图
        	title 标题
        	pic 焦点图地址
        	desc 焦点图简介
        	url 焦点图链接
        top 今日前十
        	id 影视资源ID
        	cnname 影视资源中文名
        	channel 频道 tv-电视剧,movie-电影
        	area 资源地区
        	category	资源类型
        	publish_year	上映年代
        	play_status 播放状态
        	poster 海报
        article_list 新闻资讯(第一条资讯因为是手工推荐,只有title,url,poster三个参数返回)
        	id 资讯ID
        	title 资讯标题
        	content 资讯内容(只截取了前100个文字)
        	views 浏览数
        	poster 海报
        	dateline 发布时间
        hot_comment 热门短评
        	id 短评ID
        	author 发布者UID
        	channel 资源类型,movie-电影,tv-电视剧
        	itemid 影视资源ID
        	content 短评内容
        	good 支持数
        	bad 反对数
        	dateline 发布时间
        	nickname 发布者昵称
        	avatar 发布者头像
        	group_name 所属用户组
        	cnname 影视资源中文名
        	score 评分
        	poster 对应的资源海报图
        ```
        
        ### 影视资源列表
        - 接口地址:/resource/fetchlist
        - 传递参数:
        
        ```
        channel(可选) 频道 电影:movie,电视剧:tv,公开课:openclass
        area(可选) 国家,例如:”美国”,”日本”,”英国”
        sort(可选) 排序 更新时间update,发布时间pubdate,上映时间premiere,名称name,排名rank,评分score,点击率views
        year(可选) 年代 最小值为1990
        category(可选) 影视类型 具体值请参看网站
        limit(可选) 默认为10个,不能大于20
        page(可选) 列表页码
        ```
        
        - 返回数据:
        
        ```
        id 资源ID
        cnname 中文名
        enname 英文名
        remark 说明
        area 国家
        format 格式
        category 类型
        poster 海报
        channel 频道
        lang 语言
        play_status 播放状态
        rank 排名
        score 评分
        views 浏览数
        ```
        
        ### 影视资源详情
        - 接口地址:/resource/getinfo
        - 传递参数:
        
        ```
        id(必选) 资源ID
        prevue(可选) 是否获取播放档期(只有电视剧才有效) 1-获取
        share(可选) 是否获取分享信息 1-获取
        ```
        
        - 返回数据:
        
        ```
        cnname 中文名
        enname 英文名
        remark 说明
        poster 海报
        play_status 播放状态
        area 地区
        category 类型
        views 浏览数
        score 评分
        content 简介
        prevue 播放档期
        	season 季度
        	episode 集数
        	play_time 播放时间
        	week 星期
        shareTitle 分享标题
        shareContent 分享内容
        shareImage 分享图片
        shareUrl 分享地址
        item_permission 为0表示当前用户没有权限下载资源(必须传递uid和token给当前接口),仅限IOS客户端
        ```
        
        ### 影视资源季度信息
        - 接口地址:/resource/season_episode
        - 传递参数:
        
        ```
        id(必选) 影视ID
        ```
        
        - 返回数据:
        
        ```
        season 季度
        episode 集数
        该接口会把电视剧的所有季度信息列出来(包括了单剧等),如果影视是电影则返回错误信息
        例如:{‘season’:7,’episode’:10} 表示第7季总共有10集
        ```
        
        ### 影视下载资源列表
        - 接口地址:/resource/itemlist
        - 传递参数:
        
        ```
        id(必选) 影视ID
        client(必选) 客户端类型,1-IOS,2-安卓,3-WP
        uid(必选) 用户UID
        token(必选) 用户token
        file(可选) 是否同时获取下载链接 1-获取,0-不获取
        click(可选) 部分app客户端默认只输出固定的中文字幕,更多的需要再次点击获得,click为1则表示获取更多的数据
        ```
        
        - 返回数据(电视剧的数组结构,第一层是季度信息,第二层是格式,第三层是数据列表,电影和公开课的第一层是资源格式,第二层才是数据列表):
        
        ```
        id 资源ID
        name 资源名
        format 资源格式
        season 资源季度
        episode 资源集数
        size 文件大小
        dateline 资源添加时间
        link 当需要同时获取下载链接时该参数有数据,仅限返回电驴和磁力链接
        info 如果当前用户没有足够权限获取电视剧的资源列表,该参数会输出提示用户最多只能查看资源条数的信息,默认为空
        ```
        
        ### 影视下载资源列表—不验证用户权限
        - 接口地址:/resource/itemlist_web
        - 传递参数:
        
        ```
        id(必选) 影视ID
        file(可选) 是否同时获取下载链接 1-获取,0-不获取
        season(必选) 季度
        episode(必选) 集数
        ```
        
        - 返回数据:
        
        ```
        id 资源ID
        name 资源名
        format 资源格式
        season 资源季度
        episode 资源集数
        size 文件大小
        dateline 资源添加时间
        link 当需要同时获取下载链接时该参数有数据,仅限返回电驴和磁力链接
        info 如果当前用户没有足够权限获取电视剧的资源列表,该参数会输出提示用户最多只能查看资源条数的信息,默认为空
        ```
        
        ### 影视资源下载地址
        - 接口地址:/resource/itemlink
        - 传递参数:
        
        ```
        id(必选) 资源ID
        ```
        
        - 返回参数:
        ```
        address 下载地址
        way 下载方式     1-电驴  2-磁力   9-网盘    12-城通盘
        ```
        
        ### 字幕列表
        - 接口地址:/subtitle/fetchlist
        - 传递参数:
        
        ```
        limit(可选) 数量
        page(可选) 页码
        ```
        
        - 返回数据:
        
        ```
        count 字幕总数
        list 字幕集合
        id 字幕ID
        cnname 字幕中文名
        enname 字幕英文名
        resourceid 对应的资源ID
          resource_info 资源详情
        	cnname 中文名
        	enname 英文名
        	poster 海报
        segment 对应片源
        source 字幕发布者 zimuzu(字幕组)
        category 类型
        lang 语言
        format 格式
        remark 备注
        views 浏览数
        dateline 发布时间
        ```
        
        ### 字幕详情
        - 接口地址:/subtitle/getinfo
        - 传递参数:
        
        ```
        id 字幕ID
        ```
        
        - 返回数据:
        
        ```
        id 字幕ID
        cnname 字幕中文名
        enname 字幕英文名
        resourceid 对应的资源ID
        segment 对应片源
        source 字幕发布者 zimuzu(字幕组)
        category 类型
        file 字幕文件下载地址(如果用户没权限浏览则为空)
        filename 字幕文件名
        lang 语言
        format 格式
        remark 备注
        views 浏览数
        dateline 发布时间
        protect_expire 字幕下载保护期到期时间(unix时间戳),表示当前字幕处于保护期内,用户不能查看,同时file的值为空,如为0则表示没有保护期或者已过期
        resource_info 对应的资源信息
        	cnname 中文名
        	enname 英文名
        	poster 海报
        ```
        
        ### 字幕详情—不验证用户权限
        - 接口地址:/subtitle/getinfo_web
        - 传递参数:
        
        ```
        id 字幕ID
        ```
        
        - 返回数据:
        
        ```
        id 字幕ID
        cnname 字幕中文名
        enname 字幕英文名
        resourceid 对应的资源ID
        segment 对应片源
        source 字幕发布者 zimuzu(字幕组)
        category 类型
        file 字幕文件下载地址(如果在保护期就不显示)
        filename 字幕文件名
        lang 语言
        format 格式
        remark 备注
        views 浏览数
        dateline 发布时间
        未找到索引项。
        protect_expire 字幕下载保护期到期时间(unix时间戳),表示当前字幕处于保护期内,用户不能查看,同时file的值为空,如为0则表示没有保护期或者已过期
        resource_info 对应的资源信息
        	cnname 中文名
        	enname 英文名
        	poster 海报
        ```
        
        ### 资讯列表
        - 接口地址:/article/fetchlist
        - 传递参数:
        
        ```
        newstype news-新闻,report-收视快报,m_review-影评,t_review-剧评,new_review-新剧评测,recom-片单推荐 默认为所有类型
        limit(可选) 数量
        page(可选) 页码
        ```
        
        - 返回数据:
        
        ```
        ID 资讯ID
        Title 资讯标题
        Type 资讯类型 news-新闻,guide-导视,影评-movie_review,剧评-tv_review
        Poster 海报
        Dateline	发布时间
        ```
        
        ### 资讯内容
        - 接口地址:/article/getinfo
        - 传递参数:
        
        ```
        id 资讯ID
        ```
        
        - 返回数据:
        
        ```
        id 资讯ID
        title 资讯标题
        content 资讯内容
        dateline 发布时间
        poster 海报
        resourceid 对应的影视资源ID,可能为0,表示没有关联影视资源
        ```
        
        ### 全站搜索
        - 接口地址: /search
        - 传递参数:
        
        ```
        k(必选) 搜索关键词
        st(可选) 搜索类型,resource-影视资源,subtitle-字幕资源,article-资讯以及影评和剧评.如果为空,则在以上三种资源中搜索
        order(可选) 排序 pubtime发布时间 uptime更新时间    默认为更新时间
        limit(可选) 每页数量(默认输出20个)
        page(可选) 页码
        ```
        
        - 返回数据:
        ```
        itemid 对应的资源ID
        title 资源标题
        type resource-影视资源 subtitle-字幕 article-资讯
        channel 当type为resource的时候有效,tv-电视剧,movie-电影,openclass-公开课
        pubtime 发布时间
        uptime 更新时间
        ```
        
        ### 美剧时间表
        - 接口地址:/tv/schedule
        - 传递参数:
        
        ```
        start(必选) 开始时间,标准的时间格式,如:2015-02-03或2015-2-3或20150203
        end(必选) 结束时间,同上,开始时间和结束时间不能超过31天
        limit(可选) 返回数量
        ```
        
        - 返回数据:
        
        ```
        id 电视剧ID
        cnname 电视剧中文名
        enname 电视剧英文名
        season 季度
        episode 集数
        poster 海报
        ```
        
        ### 今日热门排行
        - 接口地址:/resource/top
        - 传递参数:
        
        ```
        channel(可选) 频道 默认为电影和电视剧的排行榜  tv电视剧 movie 电影
        limit(可选) 获取数量,默认为5个
        ```
        
        - 返回数据:
        
        ```
        id 影视ID
        cnname 中文名
        channel 频道
        area 国家
        category 类型
        publish_year 发布年份
        play_status 播放状态
        ```
        
        ### 今日更新
        - 接口地址:/resource/today
        - 返回数据:
        
        ```
        resourceid 影视ID
        name 下载资源名
        format 格式
        season 季度
        episode 集数
        size 文件大小
        ways 下载方式集合   1-电驴 2-磁力
        ```
        
        ### 用户接口
        #### 用户注册
        - 接口地址:/user/register
        - 传递参数:
        
        ```
        email 邮箱
        password 密码(最少八位)
        nickname 昵称
        sex 性别 0-密码 1-男 2-女 3-其他
        source 注册来源 android-安卓客户端,ios-苹果客户端
        ```
        
        - 返回数据:
        
        ```
        uid 用户UID
        ```
        
        #### 用户登录
        - 接口地址:/user/login
        - 传递参数:
        
        ```
        account 用户账号,可以是邮箱,也可以是昵称
        password 密码
        ```
        
        - 返回数据:
        ```
        uid 用户uid
        token 登录凭证
        说明:用户最多再五台设备上登录,如有超出,第一个登录的凭证将被删除
        ```
        
        #### 退出登录
        - 接口地址:/user/logout
        - 传递参数:
        
        ```
        uid 用户uid
        token 用户登录凭证
        nickname 用户昵称
        sex 性别 0-保密 1-男 2-女 3-其他
        email 邮箱
        userpic 头像
        group_name 所属用户组
        ```
        
        #### 获取当前用户信息
        - 接口地址:/user/get_info
        - 传递参数:
        
        ```
        uid 用户uid
        token 用户登录凭证
        ```
        
        - 返回数据:
        
        ```
        uid 用户uid
        nickname 用户昵称
        sex 性别 0-保密 1-男 2-女 3-其他
        email 邮箱
        userpic 头像
        group_name 所属用户组
        ```
        
        #### 签到状态
        - 接口地址:/user/sign_status
        - 传递参数:
        
        ```
        uid 用户ID
        token 登录凭证
        ```
        
        - 返回数据:
        
        ```
        group_name 用户组
        need_day 升级所需天数
        last_sign 最近三次登录时间
        sign_times 连续签到天数
        ```
        
        #### 用户签到
        - 接口地址:/user/sign
        - 传递参数:
        
        ```
        uid 用户ID
        token 登录凭证
        ```
        
        - 返回数据:
        
        ```
        签到成功status返回1,info是签到成功的提示语
        group_name 用户组
        need_day 升级所需天数
        last_sign 最近三次登录时间
        sign_times 连续签到天数
        ```
        
        #### 获取收藏列表
        - 接口地址:/fav/fetchlist
        - 传递参数:
        
        ```
        ft 收藏类型 tv-电视剧,movie-电影,openclass-公开课 默认为空
        page 页码
        limit 每页数量
        uid 用户ID
        token 登录凭证
        ```
        
        - 返回数据:
        
        ```
        count:收藏总数
        list 收藏列表
        itemid 资源ID
        poster 资源海报
        channel 资源类型tv,movie,openclass
        area 资源地区
        cnname 资源中文名
        enname 资源英文名
        category 资源类型
        publish_year	发布年代
        remark 说明
        play_status 播放状态
        premiere 首播日期
        updatetime 更新时间
        prevue 播放时间表,可能为空
        ```
        
        #### 找回密码
        - 接口地址:/user/forget
        - 传递参数:
        
        ```
        email 邮箱账号
        ```
        
        - 返回数据:
        
        ```
        status-返回状态,info-提示信息,操作成功后回提示用户去邮箱查看找回密码的链接
        ```
        
        #### 收藏状态
        - 接口地址:/fav/check_follow
        - 传递参数:
        
        ```
        id 影视资源ID
        ```
        
        - 返回数据:
        
        ```
        data 1-已收藏 0-未收藏
        ```
        
        #### 收藏资源
        - 接口地址:/fav/follow
        - 传递参数:
        
        ```
        id 资源ID
        ```
        
        - 返回数据:
        
        ```
        status为1则表示操作成功
        ```
        
        #### 取消收藏
        - 接口地址:/fav/unfollow
        - 传递参数:
        
        ```
        id 资源ID
        ```
        
        - 返回数据:
        
        ```
        status为1则表示操作成功
        ```
        
        ### 短评接口
        #### 获取短评
        短评接口是全站短评通用的接口,不再对影视或字幕等做单独的接口.无论当前用户是否登录,调用短评接口都需要uid和token两个参数
        返回的参数中status为1,则表示返回正常,否则会返回失败原因,其他短评接口相同
        
        - 接口地址:/comment/fetch
        - 传递参数:
        
        ```
        channel 频道,article-资讯,openclass-公开课,tv-电视剧,movie-电影,subtitle-字幕
        itemid 对应的资源ID
        pagesize 每页数量
        page(可选) 页码,默认为最后一页
        ```
        
        - 返回数据:
        
        ```
        count 短评总数
        pageCount 总页码数
        page 当前页数
        pagesize 每页短评数
        list 短评数组
        	id 短评ID
        	author 发布人UID
        	nickname 发布人昵称
        	avatar 发布人头像
        	content 短评内容
        	good 支持数
        	bad 反对数
        	dateline 短评发布时间
        	hot 1-热门短评,只有在page为第一页,最后一页或者未输入值的时候才有数据
        	reply 该短评的回复评论,返回的参数与上面类似
        	avatar 头像
        	group_name 所属用户组
        ```
        
        #### 保存短评
        
        - 接口地址:/comment/save
        - 传递参数:
        
        ```
        channel 频道,article-资讯,openclass-公开课,tv-电视剧,movie-电影,subtitle-字幕
        itemid 对应的资源ID
        content 短评内容
        replyid 如果是回复短评,则为对应的短评ID,否则为0
        ```
        
        #### 更新短评
        - 接口地址:/comment/update
        - 传递参数:
        
        ```
        commentId 短评ID
        content 短评内容
        ```
        
        #### 删除短评
        - 接口地址:/comment/delete
        - 传递参数:
        
        ```
        id 短评ID
        ```
        
        #### 支持短评
        - 接口地址:/comment/good
        - 传递参数:
        
        ```
        id 短评ID
        ```
        
        #### 反对短评
        - 接口地址:/comment/bad
        - 传递参数:
        
        ```
        id 短评ID
        ```
        
        ### 网站配置
        以下接口都不需要权限验证,可以直接访问获取
        
        #### 网站全局参数
        - 接口地址:/config/app
        
        #### 资源类型
        - 接口地址:/config/resource_category
        
        #### 资源地区
        - 接口地址:/config/resource_area
        
        #### 资源格式
        - 接口地址:/config/resource_format
        
        #### 资源语言
        - 接口地址:/config/resource_lang
        
        #### 资源电视台
        - 接口地址:/config/resource_tv
        
        #### 广告内容
        - 接口地址:/ad
        - 返回数据:
        
        ```
        index 首页
        resource_list 影视资源列表
        resource_show 影视资源详情页
        resource_file_show 影视资源文件详情
        schedule 时间表
        subitlte_show 字幕详情页
        sign 签到页
        fav 我的收藏
        以上每个参数又对应了link和pic两个,分别为广告链接和广告图片
        ```
        
        #### 版本检查
        - 接口地址:/version/check
        - 传递参数:
        
        ```
        vcode:版本号,使用整形数字
        ```
        
        - 返回数据:
        
        ```
        need_update:是否需要更新 true-需要,false-不需要
        download_url:下载地址
        version:最新版本号
        content:更新信息
        ```
        
        
        ### 0.0.1 (20161209)
        
        - 项目初始化
        
Keywords: zimuzu,api,sdk,service
Platform: any
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: Topic :: Software Development :: SDK
Classifier: License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Requires-Python: >=3.3
