# Creator-Specific Supabase API Setup Guide

## 🎯 **Overview**

Each creator now has their own separate Supabase project and API configuration. This allows:
- Independent knowledge bases per creator
- Better scalability
- Isolated data per creator
- Easier management

## 🔧 **Quick Setup**

### **1. Add MKBHD API (Testing)**

```bash
python setup_creator_api.py
```

Enter your MKBHD Supabase URL and key when prompted.

### **2. Manual Setup**

Edit `creator_config.py`:

```python
CREATOR_SUPABASE_CONFIG = {
    "Marques Brownlee": {
        "supabase_url": "https://your-mkbhd-project.supabase.co",
        "supabase_key": "your-mkbhd-anon-key-here",
    },
    # Add other creators as needed
}
```

## 📝 **How It Works**

### **When a user selects a creator:**

1. **System looks up the creator** → Finds their specific Supabase config
2. **Creates a Supabase client** → Uses that creator's API credentials
3. **Searches their knowledge base** → Only their content is retrieved
4. **Returns their knowledge** → Creator-specific context

### **Example Flow:**

```
User selects: "Marques Brownlee"
User asks: "What's the best iPhone camera?"

System:
1. Looks up "Marques Brownlee" config
2. Connects to MKBHD's Supabase
3. Searches MKBHD's knowledge base
4. Finds: "iPhone 15 Pro has 48MP camera..."
5. Returns: MKBHD's actual knowledge about iPhone cameras
```

## 🔑 **Getting Supabase Credentials**

### **For each creator:**

1. **Create a Supabase project** for that creator
2. **Get Project URL**: Found in Settings → API
3. **Get Anon Key**: Found in Settings → API

### **MKBHD Example:**
```python
"supabase_url": "https://mkbhd-knowledge-base.supabase.co"
"supabase_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## ✅ **Testing**

### **Test if API is configured:**

```bash
python -c "from creator_config import get_creator_config; print(get_creator_config('Marques Brownlee'))"
```

### **Test the full flow:**

```bash
# Start server
python server.py

# Chat with MKBHD about iPhone cameras
# Should retrieve MKBHD's actual knowledge
```

## 🎯 **Adding More Creators**

### **Step 1: Create Supabase project**
- One project per creator
- Set up the schema (from `supabase_schema.sql`)

### **Step 2: Add credentials**
```bash
python setup_creator_api.py
```

Or edit `creator_config.py` directly.

### **Step 3: Populate knowledge**
```bash
python setup_embeddings.py
```

### **Step 4: Test**
- Chat with that creator
- Verify knowledge retrieval works

## 📊 **Current Status**

| Creator | API Configured | Status |
|---------|----------------|--------|
| Marques Brownlee | ⏳ Ready for setup | Awaiting credentials |
| Austin Evans | ❌ Not configured | Add when ready |
| Justine Ezarik | ❌ Not configured | Add when ready |
| Zack Nelson | ❌ Not configured | Add when ready |
| Lewis George Hilsenteger | ❌ Not configured | Add when ready |

## 🔍 **Debugging**

### **If no knowledge found:**

1. **Check API credentials**:
   ```python
   from creator_config import get_creator_config
   print(get_creator_config("Marques Brownlee"))
   ```

2. **Check Supabase connection**:
   - Look for logs: "✅ Supabase client created for {creator}"
   - If missing, credentials might be wrong

3. **Check knowledge base**:
   - Verify schema is set up
   - Verify embeddings are populated
   - Verify creator_id matches

### **Common Issues:**

- **"No Supabase configuration"** → Run `python setup_creator_api.py`
- **"Supabase client failed"** → Check credentials
- **"No knowledge found"** → Run `python setup_embeddings.py`

## 🚀 **Next Steps**

1. **Add MKBHD API** (You have the credentials)
2. **Test with real queries**
3. **Add remaining creators** as needed
4. **Monitor knowledge retrieval** success rates
