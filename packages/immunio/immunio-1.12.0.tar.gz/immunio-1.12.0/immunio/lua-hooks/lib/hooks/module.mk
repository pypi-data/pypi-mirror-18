MODULES := lib/hooks/xss

LUA_SRC += \
	lib/hooks/authenticate.lua \
	lib/hooks/bad_cookie.lua \
	lib/hooks/custom_event.lua \
	lib/hooks/custom_threat.lua \
	lib/hooks/encode.lua \
	lib/hooks/eval.lua \
	lib/hooks/exception.lua \
	lib/hooks/file_io.lua \
	lib/hooks/framework_csrf_check.lua \
	lib/hooks/framework_login.lua \
	lib/hooks/framework_password_reset.lua \
	lib/hooks/framework_account_created.lua \
	lib/hooks/framework_redirect.lua \
	lib/hooks/framework_session.lua \
	lib/hooks/framework_user.lua \
	lib/hooks/framework_route.lua \
	lib/hooks/framework_bad_response_header.lua \
	lib/hooks/http_request_finish.lua \
	lib/hooks/http_request_start.lua \
	lib/hooks/http_response_start.lua \
	lib/hooks/mongodb_execute.lua \
	lib/hooks/should_report.lua \
	lib/hooks/sql_execute.lua \
	lib/hooks/template_render_done.lua \
	lib/hooks/xss/escape.lua \
	lib/hooks/xss/escape_js.lua \

include $(patsubst %, %/module.mk,$(MODULES))
