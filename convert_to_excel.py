import logging
import pandas as pd

# フォーマット設定
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.ERROR, format=log_format)
# タグIDなどの情報を取得し、DataFrameに格納する関数
def extract_tags(file_data):
    # print("Received file path:", file_data)

    try:
        if file_data:
            # JSONデータの処理を行う
            container_version = file_data['containerVersion']
            data_tag = container_version['tag']
            data_trigger = container_version['trigger']

            # triggerIdをtriggerNameにマッピングする辞書を作成する
            trigger_dict = {}
            for trigger in data_trigger:
                trigger_dict[trigger['triggerId']] = trigger['name']

            # data_tagのリストに含まれる各tag_listを処理する
            tag_dicts = []
            for tag_list in data_tag:
                # tag_listからfiringTriggerIdを取り出す
                firingTriggerIds = tag_list['firingTriggerId']
                # firingTriggerIdsを使ってtriggerNamesのリストを生成する
                triggerNames = [trigger_dict[firingTriggerId] for firingTriggerId in firingTriggerIds if firingTriggerId in trigger_dict]

                # タグごとの辞書を作成してtag_dictsに追加する
                tag_dict = {
                    'タグID': tag_list['tagId'],
                    'タグ名': tag_list['name'],
                    '設置タグ': tag_list['parameter'][0]['value'],
                    #'トリガーID': firingTriggerIds,
                    'トリガー名': '\n'.join(triggerNames),
                    'トリガー': ''  # 初期化
                }

                # タグに関連するトリガーがある場合、フィルターの'value'を取得する
                for trigger_id in firingTriggerIds:
                    for trigger in data_trigger:
                        if trigger['triggerId'] == trigger_id and 'filter' in trigger:
                            filter_value = trigger['filter'][0].get('parameter', [{}])[1].get('value', '')
                            tag_dict['トリガー'] += f"\n{trigger_id}: {filter_value}"

                tag_dicts.append(tag_dict)

                 # 辞書のリストをDataFrameに変換する
            df = pd.DataFrame(tag_dicts)
            

            print(df)
            return df

    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

    return None

