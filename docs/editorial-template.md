# 口播网感模板

本次新增的是既有 `video-compose-render` 的可选参数，不新增任意命令执行入口。
用户上传带原声的 9:16 口播视频，由 Agent 准备中英双语字幕和真实词级关键词动作计划，
服务保留人物和原声，按已确认 EDL 输出 720×1280、30fps MP4。首版支持 3–180 秒。

## 发现与调用

```sh
hq describe video-compose-import --json
hq describe video-compose-render --json
hq run video-compose-import --file /absolute/path/talking.mp4 --confirm --json
hq run video-compose-create --input @create.json --confirm --json
hq run video-compose-analyze --input @analyze.json --confirm --json
hq run video-compose-project --input @project.json --json
hq run video-compose-review --input @review.json --confirm --json
hq run video-compose-project --input @project.json --json
hq run video-compose-render --input @render.json --confirm --json
hq run video-compose-project --input @project.json --json
```

使用前须取得用户对上传、外部转写和剪辑处理的确认。上传响应的资产 ID 用于 create；
创建响应的 project_id 用于后续操作；每次读最新 revision。默认所有候选选 keep，
只有用户确认删除的片段才选 remove。没有候选时 review 的 decisions 可以为 {}。
本 CLI 不自行识别语音、翻译或等待渲染完成；这些由 Agent 编排与主站执行。

`render.json` 示例（ID、hash 和时间均为示意，不能替代实际项目数据）：

```json
{
  "project_id": "compose_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "expected_revision": 3,
  "template_id": "ip-editorial-serif-v1",
  "editorial_plan": {
    "schema": "hq.editorial-plan/v1",
    "timebase": "edited_output",
    "transcript_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "edit_decision_version": 1,
    "title": ["一个人的效率", "内容更有价值"],
    "captions": [{"start": 0.5, "end": 3, "text": "一个人", "en": "One person"}],
    "keywords": ["一个人"],
    "camera": [{"at": 0, "scale": 1, "transition": "cut"}],
    "keyword_punches": [{"at": 0.5, "word": "一个人", "strength": 1.075}],
    "callouts": []
  }
}
```

Agent 必须使用当前转写 hash、已确认 EDL 版本和**剪辑后秒级时间**。
keywords 来自当前字幕；动作起点须有真实词级时间证据，按句长均分的估算不可冒充。
必须提供准确英文翻译，不能只传 template_id，也不能提交 HTML、JS、路径或命令。
完整字段、数量和范围以 `hq describe video-compose-render --json` 为准。
不传新参数时，旧渲染请求仍兼容。

成功提交后保存 project_id，只用 video-compose-project 轮询；不是通用 task/job_id。
completed 后检查 quality.decision、output_asset_id、output_url，再交付可鉴权读取的作品。
409 先读取旧任务，禁止换计划盲目重试；failed 先读最新 revision 再重试。

## 发布边界

本 PR 准备公共 CLI 0.15.7 候选包，不自动发布 tag/release，也不部署服务器。
后端必须先有相同能力；客户端能校验新参数不代表生产渲染器已安装。
正式主/子 Agent 的“口播网感模板”名称路由仍须在它自己的正式源码仓库接入。

已只读核对独立 Agent Skill 主线 manifest：Skill 0.4.0，tested/latest/installer CLI 0.15.0。
这不是对 0.15.7 的兼容性认证。发布时需在独立仓库验证并更新 manifest，
不要在 CLI 内复制第二份 canonical Skill，也不要把未验证版本写成 tested。
