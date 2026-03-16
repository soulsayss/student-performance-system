# ⚡ Deployment Quick Reference

## Your URLs

**Frontend (Vercel):**
```
https://student-performance-system-kohl.vercel.app
```

**Backend (Render):** (after deployment)
```
https://your-service-name.onrender.com
```

## Admin Credentials

```
Email: admin@school.edu
Password: Admin@123
```

⚠️ Change password after first login!

## Key Files

| File | Location | Purpose |
|------|----------|---------|
| Procfile | `backend/` | Start command |
| render.yaml | `backend/` | Deployment config |
| init_db.py | `backend/` | Database setup |
| config.py | `backend/` | Database config |
| app.py | `backend/` | CORS settings |

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created on Render
- [ ] Environment variables set
- [ ] Deployment complete (shows "Live")
- [ ] Database initialized (`python init_db.py`)
- [ ] `/health` endpoint working
- [ ] Admin user created
- [ ] Frontend API URL updated
- [ ] Frontend redeployed
- [ ] Login test successful

## Environment Variables (Render)

```
FLASK_ENV = production
SECRET_KEY = (auto-generated)
JWT_SECRET_KEY = (auto-generated)
DATABASE_URL = (auto-provided by Render)
```

## Testing Commands

**Check backend health:**
```bash
curl https://your-service-name.onrender.com/health
```

**Expected response:**
```json
{"status": "healthy"}
```

## Common Commands

**Initialize database:**
```bash
python init_db.py
```

**View logs:**
- Go to Render dashboard
- Click your service
- Click "Logs" tab

**Restart service:**
- Go to Render dashboard
- Click your service
- Click "Restart" button

## CORS Configuration

Your Vercel frontend is already allowed:
```
https://student-performance-system-kohl.vercel.app
```

Plus:
- `http://localhost:3000` (local dev)
- `https://*.vercel.app` (other Vercel apps)

## Database

- **Type:** PostgreSQL
- **Provider:** Render (automatic)
- **Storage:** 1GB free
- **Backups:** Automatic

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build failed | Check `requirements.txt` in `backend/` |
| Won't start | Check `Procfile` exists |
| Admin creation failed | Run `python init_db.py` again |
| CORS errors | Your URL is already added |
| Can't connect DB | DATABASE_URL is auto-set |

## Important Notes

1. **First deployment takes 2-5 minutes**
2. **Free tier spins down after 15 min inactivity**
3. **First request after spin-down takes 30 seconds**
4. **Data persists between deployments**
5. **Change admin password after login**

## Next Steps

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Connect your GitHub repo
5. Set environment variables
6. Deploy
7. Run `python init_db.py`
8. Update frontend API URL
9. Test everything

---

**Everything is ready! Deploy now! 🚀**
