import json

from mitmproxy import master, http

from masterController import run


class IDVaddon:
    @staticmethod
    def request(flow: http.HTTPFlow):
        if "mpay" in flow.request.url and 'qrcode' not in flow.request.url:
            cv = flow.request.query.get("cv", None)
            if cv is not None:
                flow.request.query["cv"] = cv.replace("c", "p")
                flow.request.query.pop("arch", None)

                print("query:", flow.request.query)
            
            if flow.request.method == "POST":
                print("old_body:", flow.request.get_text())

                new_body = dict(x.split("=") for x in flow.request.get_text().split("&"))

                new_body["cv"] = new_body.get("cv", "").replace("c", "p")
                new_body.pop("arch", None)

                flow.request.set_text("&".join([f"{k}={v}" for k, v in new_body.items()]))

                print("new_body:", new_body)

        return None

    @staticmethod
    def response(flow: http.HTTPFlow):
        if 'login_methods' in flow.request.url:
            new_login_methods = json.loads(flow.response.get_text())
            new_login_methods["select_platform"] = True
            new_login_methods["qrcode_select_platform"] = True
            for i in new_login_methods["config"]:
                new_login_methods["config"][i]["select_platforms"] = [0, 1, 2, 3, 4]
            flow.response.set_text(json.dumps(new_login_methods))

            return None

        if 'pc_config' in flow.request.url:
            new_pc_config = json.loads(flow.response.get_text())
            new_pc_config["game"]["config"]["cv_review_status"] = 1
            flow.response.set_text(json.dumps(new_pc_config))

            return None

        if 'devices' in flow.request.url:
            Info = {
                "extra_unisdk_data": "",
                "from_game_id": "h55",
                "src_app_channel": "netease",
                "src_client_ip": "",
                "src_client_type": 1,
                "src_jf_game_id": "h55",
                "src_pay_channel": "netease",
                "src_sdk_version": "3.15.0",
                "src_udid": ""
            }

            new_devices = json.loads(flow.response.get_text())
            new_devices["user"]["pc_ext_info"] = Info
            flow.response.set_text(json.dumps(new_devices))

            return None


def callback(the_master: master.Master):
    the_master.addons.add(IDVaddon())
    return None


def launch():
    args = ["--mode", "transparent", "--allow-hosts", "service.mkey.163.com"]
    run(args, callback)
