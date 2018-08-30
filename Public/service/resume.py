table_config = [
            {
                'q': None,  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "<input type='checkbox' />", 'kwargs': {}}, # 一个@符号表示取数据库内的数据，两个 @ 符号表示取全局变量中与自身相等的文本信息
                'attr': {}  # 自定义属性
            },            
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "序号",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}}, # 一个@符号表示取数据库内的数据，两个 @ 符号表示取全局变量中与自身相等的文本信息
                'attr': {
                    "edit-enable": "true",
                    "resume-id": "@id",
                    # "style": "display: none;"
                }
            },            
            {
                'q': ['custom_label__name', 'custom_label__code', 'custom_label__priority', 'agent'],
                'title': "",
                'display': 1,
                # 'text': {'content': "{n}{m}{o}", 'kwargs': {'n': '@custom_label__name', 'm': '@custom_label__code', 'o': '@custom_label__priority'}},
                'text': {'content': "{n}", 'kwargs': {'n': '@custom_label'}},
                'attr': {},
            },   
            {
                'q': 'username',
                'title': "姓名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@username'}},
                'attr': {},
            },
            {
                'q': 'jobs',
                'title': "目前职位",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@jobs'}},
                'attr': {},
            },
            {
                'q': 'gender',
                'title': "性别",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@gender'}},
                'attr': {}
            },
            {
                'q': 'age',
                'title': "年龄",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@age'}},
                'attr': {}
            },
            {
                'q': 'phone',
                'title': "电话",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@phone'}},
                'attr': {
                    'edit-enable': 'true',
                    'edit-type': 'input',
                    'name': 'phone',
                    'origin': '@phone',
                },
            },
            {
                'q': 'email',
                'title': "Email",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@email'}},
                'attr': {
                    'edit-enable': 'true',
                    'edit-type': 'input',
                    'name': 'email',
                    'origin': '@email',
                },
            },
            # {
            #     'q': 'cnterview_time',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
            #     'title': "约谈时间",  # 前段表格中显示的标题
            #     'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
            #     'text': {'content': "{n}", 'kwargs': {'n': '@cnterview_time'}}, # 一个@符号表示取数据库内的数据，两个 @ 符号表示取全局变量中与自身相等的文本信息
            #     'attr': {
            #         'edit-enable': 'true',
            #         'edit-type': 'input',
            #         'name': 'cnterview_time',
            #         'origin': '@cnterview_time',
            #     },
            # },
            # {
            #     'q': 'track_progress',
            #     'title': "跟踪进度",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@track_progress'}},
            #     'attr': {
            #         'edit-enable': 'true',
            #         'edit-type': 'input',
            #         'name': 'track_progress',
            #         'origin': '@track_progress',
            #     },
            # },
            # {
            #     'q': 'resume_source',
            #     'title': "简历来源",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@resume_source'}},
            #     'attr': {
            #         'edit-enable': 'true',
            #         'edit-type': 'input',
            #         'name': 'resume_source',
            #         'origin': '@resume_source',
            #     },
            # },
            {
                'q': 'resume_status',
                'title': "流程",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@resume_status_choices'}},
                'attr': {
                    'edit-enable': 'true',
                    'edit-type': 'select',
                    'global-name': "resume_status_choices",
                    'origin': '@resume_status',
                    'name': 'resume_status',
                },
            },


            # {
            #     'q': 'cc__set',
            #     'title': "候选人",
            #     'display': 1,
            #     'text': {'content': "{n}", 'kwargs': {'n': '@candidate__name'}},
            #     'attr': {}
            # },
            {
                'q': 'create_time',
                'title': "上传时间",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@create_time'}},
                'attr': {},
            },
            {
                'q': ['user_comments__describe', 'user_comments__user', 'user_comments__create_time', 'user_comments__user__email', 'user_comments__user__head_portrait'],
                'title': "",
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@user_comments'}},
                'attr': {
                    
                },
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': '''<td class="actions"><a href="candidate/{uid}/change" class="on-default edit-row" data-toggle="tooltip" data-placement="top" title="" data-original-title="Edit"><i class=""></i>编辑</a></td>''',
                    'kwargs': {'device_type_id': '@device_type_id', 'uid': '@id'}},
                'attr': {}
            },
        ]