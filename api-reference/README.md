# The Cat API 开发者集成指南

> **文档版本**: 1.0.0   
> **API Base URL**: `https://api.thecatapi.com/v1`

## 1. 简介 (Introduction)
The Cat API 是一个为开发者提供的免费 RESTful API，用于在您的应用或网站中集成猫咪图片、品种信息及相关数据。它常用于演示、测试以及构建宠物相关的应用程序。

本指南将帮助您快速了解如何进行身份验证、搜索图片以及与数据交互。

---

## 2. 认证与鉴权 (Authentication)

### 2.1 为什么需要 API Key？
虽然 The Cat API 的部分 GET 请求（如获取随机图片）是公开的，但为了**防止滥用**并**区分不同用户**，API 使用 API Key 来进行速率限制（Rate Limiting）。

* **无 Key 用户**: 访问受限，无法使用投票/收藏等写入功能。
* **有 Key 用户**: 享有更高的请求配额和完整的写入权限。

### 2.2 如何使用
在发送 HTTP 请求时，请将您的 API Key 添加到请求头（Header）中：

- **Header Name**: `x-api-key`
- **Value**: `您的_API_KEY_字符串`

> **安全提示**: 请勿将您的 API Key 直接暴露在前端代码（如 HTML/JS）中，建议通过后端代理请求以保护您的密钥安全。

---

## 3. 接口参考 (Endpoints)

### 3.1 图片搜索 (Images)
这是 API 最核心的功能，用于检索符合特定条件的猫咪图片。

**端点**: `GET /images/search`

#### 请求参数 (Query Parameters)
通过在 URL 后拼接参数来过滤结果。例如：`?limit=5&breed_ids=beng`。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| `limit` | Integer | 否 | 1 | 返回图片的数量 (最大 10) |
| `page` | Integer | 否 | 0 | 用于分页的页码 |
| `order` | String | 否 | RAND | 排序方式: `ASC`(升序), `DESC`(降序), `RAND`(随机) |
| `breed_ids`| String | 否 | - | 按品种 ID 过滤 (如 `beng` 代表孟加拉猫) |
| `mime_types`| String | 否 | jpg,png | 过滤文件类型: `jpg`, `png`, `gif` |

#### 请求示例
获取 3 张包含“孟加拉猫”品种信息的图片：

```bash
curl --location --request GET "https://api.thecatapi.com/v1/images/search?limit=3&breed_ids=beng" --header "x-api-key: YOUR_API_KEY"
```

> **⚠️ Windows 用户提示**:
> 如果您在 PowerShell 中运行遇到报错，请尝试使用 `curl.exe` 代替 `curl`，或在命令中添加 `-k` 参数忽略 SSL 证书检查（仅限本地测试）。
> 若一行命令太长，为了显示美观，可以使用反引号 `` ` `` 换行，Linux/Mac 用户则可用 `\` 换行。

#### 响应示例 (JSON)
成功请求将返回 `200 OK`。

```json
[
  {
    "id": "J2PmlIizw",
    "url": "https://cdn2.thecatapi.com/images/J2PmlIizw.jpg",
    "width": 1080,
    "height": 1350,
    "breeds": [
      {
        "id": "beng",
        "name": "Bengal",
        "temperament": "Alert, Agile, Energetic, Demanding, Intelligent"
      }
    ]
  }
]
```

---

### 3.2 投票 (Votes)
允许已认证的用户对特定图片进行“赞”或“踩”的操作。这是一个典型的 **POST** 请求，需要携带数据体（Body）。

**端点**: `POST /votes`

#### 请求体 (Body Parameters)
格式必须为 `application/json`。

| 参数名 | 类型 | 必填 | 说明 |
| :---: | :---: | :---: | :---: |
| `image_id` | String | **是** | 你想要投票的图片 ID |
| `sub_id` | String | 否 | 自定义用户 ID (用于区分您应用下的不同用户) |
| `value` | Integer | **是** | `1` 代表赞 (Upvote), `0` 代表踩 (Downvote) |

#### 请求示例

```bash
curl --location --request POST "https://api.thecatapi.com/v1/votes" --header "x-api-key: YOUR_API_KEY" --header "Content-Type: application/json" --data-raw
"{
    \"image_id\": \"asf2\",
    \"value\": 1
}"
```

#### 响应示例
成功创建投票将返回 `201 Created`。

```json
{
  "message": "SUCCESS",
  "id": 12345,
  "image_id": "asf2",
  "value": 1,
  "country_code": "US"
}
```

---

## 4. 错误处理 (Error Handling)

当 API 请求失败时，会返回相应的 HTTP 状态码。建议开发者在代码中妥善处理这些错误。

| 状态码 | 含义 | 说明 |
| :---: | :---: | :---: |
| **200** | OK | 请求成功 |
| **201** | Created | 资源创建成功 (如投票成功) |
| **400** | Bad Request | 请求参数有误 (请检查 Body 格式或必填项) |
| **401** | Unauthorized | 缺少 API Key 或 Key 无效 |
| **404** | Not Found | 请求的资源不存在 |
| **500** | Server Error | API 服务器内部错误 |

---

*文档由 [Franita] 整理编写。*