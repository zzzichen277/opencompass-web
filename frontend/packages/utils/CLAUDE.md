[根目录](../../CLAUDE.md) > **packages** > **utils**

# @sa/utils 模块文档

> 最后更新: 2026-03-05

## 模块职责

提供通用工具函数，包括：
- 加密解密（AES）
- 本地存储封装
- 唯一 ID 生成
- 对象深拷贝

## 入口与启动

**入口文件**: `src/index.ts`

```typescript
export * from './crypto';
export * from './storage';
export * from './nanoid';
export * from './klona';
```

## 对外接口

### crypto 模块

AES 加密解密工具。

```typescript
import { encrypt, decrypt } from '@sa/utils';

const encrypted = encrypt(data, key);
const decrypted = decrypt(encrypted, key);
```

### storage 模块

本地存储封装，支持前缀隔离。

```typescript
import { localStg, sessionStg } from '@sa/utils';

localStg.set('key', value);
localStg.get('key');
localStg.remove('key');
localStg.clear();
```

### nanoid 模块

唯一 ID 生成器。

```typescript
import { nanoid } from '@sa/utils';

const id = nanoid(); // 21 字符唯一 ID
const id = nanoid(10); // 指定长度
```

### klona 模块

对象深拷贝。

```typescript
import { klona } from '@sa/utils';

const cloned = klona(originalObject);
```

## 关键依赖与配置

### 依赖

| 包名 | 用途 |
|------|------|
| `crypto-js` | AES 加密 |
| `nanoid` | ID 生成 |
| `klona` | 深拷贝 |

### 配置

存储前缀由环境变量 `VITE_STORAGE_PREFIX` 控制，默认 `SOY_`。

## 数据模型

```typescript
// 存储接口
interface StorageLike {
  get<T>(key: string): T | null;
  set<T>(key: string, value: T): void;
  remove(key: string): void;
  clear(): void;
}

// localStg / sessionStg 实现此接口
```

## 测试与质量

- 未配置单元测试
- 使用 TypeScript 严格模式

## 常见问题 (FAQ)

**Q: 如何修改存储前缀？**
在 `.env` 文件中设置 `VITE_STORAGE_PREFIX=YOUR_PREFIX_`。

**Q: 存储的数据类型限制？**
支持任何可 JSON 序列化的数据类型。

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/index.ts` | 主入口 |
| `src/crypto.ts` | AES 加密解密 |
| `src/storage.ts` | 本地存储封装 |
| `src/nanoid.ts` | ID 生成器 |
| `src/klona.ts` | 深拷贝 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |