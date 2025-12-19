import numpy as np
import random

def im2double(img):

    img = np.asarray(img, dtype=np.float64)
    if img.max() > 1.0:
        img /= 255.0
    return img


def quilt_random(sample, outsize, patchsize):

    samp = im2double(sample)
    Hs, Ws, C = samp.shape
    Hout, Wout = outsize
    ph, pw = patchsize, patchsize if isinstance(patchsize, int) else patchsize
    result = np.zeros((Hout, Wout, C), dtype=np.float64)


    for y in range(0, Hout, ph):
        for x in range(0, Wout, pw):
            i = np.random.randint(0, Hs - ph + 1)
            j = np.random.randint(0, Ws - pw + 1)
            result[y:y+ph, x:x+pw] = samp[i:i+ph, j:j+pw]
    return result


def quilt_simple(sample, outsize, patchsize, overlap, tol):

    samp = im2double(sample)
    Hs, Ws, C = samp.shape
    Hout, Wout = outsize
    ph, pw = patchsize, patchsize if isinstance(patchsize, int) else patchsize
    step_y = ph - overlap
    step_x = pw - overlap
    result = np.zeros((Hout, Wout, C), dtype=np.float64)


    i0 = np.random.randint(0, Hs - ph + 1)
    j0 = np.random.randint(0, Ws - pw + 1)
    result[0:ph,0:pw] = samp[i0:i0+ph, j0:j0+pw]


    for y in range(0, Hout, step_y):
        for x in range(0, Wout, step_x):
            if y==0 and x==0:
                continue

            region = result[y:y+ph, x:x+pw]
            ry, rx = region.shape[:2]

            costs = []
            patches = []
            for i in range(0, Hs - ry + 1):
                for j in range(0, Ws - rx + 1):
                    cand = samp[i:i+ry, j:j+rx]
                    ssd = 0

                    if x>0:
                        left = result[y:y+ry, x:x+overlap]
                        cand_left = cand[:, :overlap]
                        ssd += np.sum((left - cand_left)**2)

                    if y>0:
                        top = result[y:y+overlap, x:x+rx]
                        cand_top = cand[:overlap, :]
                        ssd += np.sum((top - cand_top)**2)
                    costs.append(ssd)
                    patches.append(cand)
            costs = np.array(costs)
            thresh = costs.min() * (1 + tol)
            idx = np.where(costs <= thresh)[0]
            sel = idx[np.random.randint(len(idx))]
            result[y:y+ry, x:x+rx] = patches[sel]
    return result


def cut(cost):

    H, W = cost.shape
    dp = cost.copy()
    path = np.zeros((H, W), dtype=int)

    for i in range(1, H):
        for j in range(W):
            min_val = dp[i-1, j]
            idx = j
            if j > 0 and dp[i-1, j-1] < min_val:
                min_val = dp[i-1, j-1]
                idx = j-1
            if j < W-1 and dp[i-1, j+1] < min_val:
                min_val = dp[i-1, j+1]
                idx = j+1
            dp[i, j] += min_val
            path[i, j] = idx


    mask = np.zeros((H, W), dtype=bool)
    j = np.argmin(dp[-1])
    for i in range(H-1, -1, -1):
        mask[i, :j] = True
        j = path[i, j]

    return mask



def quilt_cut(sample, outsize, patchsize, overlap, tol=0.1, max_cand=200):

    samp = im2double(sample)
    Hs,Ws,C = samp.shape
    ph = pw = patchsize if isinstance(patchsize,int) else patchsize
    Hout,Wout = outsize
    step = ph-overlap
    result = np.zeros((Hout,Wout,C),dtype=np.float64)

    i0,j0 = random.choice([(i,j) for i in range(Hs-ph+1) for j in range(Ws-pw+1)])
    result[:ph,:pw] = samp[i0:i0+ph, j0:j0+pw]

    cand = [(i,j) for i in range(Hs-ph+1) for j in range(Ws-pw+1)]
    for y in range(0,Hout,step):
        for x in range(0,Wout,step):
            if y==0 and x==0: continue
            ry,rx = min(ph,Hout-y), min(pw,Wout-x)
            best=(None, np.inf, None)
            random.shuffle(cand)
            for i,j in cand[:max_cand]:
                cand = samp[i:i+ry,j:j+rx]
                cost = np.zeros((ry,rx))
                if x>0:
                    ow = min(overlap,x,rx)
                    cost[:,:ow] = np.sum((result[y:y+ry, x-ow:x]-cand[:,:ow])**2,axis=2)
                if y>0:
                    oh = min(overlap,y,ry)
                    cost[:oh,:] += np.sum((result[y-oh:y, x:x+rx]-cand[:oh,:])**2,axis=2)
                m = cut(cost)
                val = cost[m].sum()
                if val<best[1]: best=(cand.copy(),val,m.copy())
            best_patch,_,best_mask = best
            old = result[y:y+ry, x:x+rx].copy()
            mask2 = np.zeros((ry,rx),bool)
            if x>0: mask2[:,:ow]=True
            if y>0: mask2[:oh,:]=True
            res = old.copy()
            res[~mask2] = best_patch[~mask2]
            res[mask2&best_mask] = best_patch[mask2&best_mask]
            result[y:y+ry, x:x+rx] = res
    return result


def texture_transfer(sample, target, patchsize, overlap, tol, alpha=0.5, max_cand=200):

    samp = im2double(sample); tgt = im2double(target)
    Ht,Wt,C = tgt.shape; ph=pw=patchsize
    step = ph-overlap
    lumt = tgt.mean(axis=2)
    result = np.zeros((Ht,Wt,C),dtype=np.float64)
    result[:ph,:pw] = samp[:ph,:pw]
    cand = [(i,j) for i in range(0,samp.shape[0]-ph+1) for j in range(0,samp.shape[1]-pw+1)]
    for y in range(0,Ht,step):
        for x in range(0,Wt,step):
            if y==0 and x==0: continue
            ry,rx = min(ph,Ht-y), min(pw,Wt-x)
            region = result[y:y+ry, x:x+rx]
            lum_bl = lumt[y:y+ry, x:x+rx]
            best = (None,np.inf,None)
            random.shuffle(cand)
            for i,j in cand[:max_cand]:
                cand = samp[i:i+ry,j:j+rx]
                cost = np.zeros((ry,rx))
                if x>0:
                    ow=min(overlap,x,rx)
                    cost[:,:ow] = np.sum((region[:,:ow]-cand[:,:ow])**2,axis=2)
                if y>0:
                    oh=min(overlap,y,ry)
                    cost[:oh,:] += np.sum((region[:oh,:]-cand[:oh,:])**2,axis=2)
                lum_er = np.sum((cand.mean(axis=2)-lum_bl)**2)
                score = (1-alpha)*cost.sum() + alpha*lum_er
                if score<best[1]:
                    mask2 = np.zeros((ry,rx),bool)
                    if x>0: mask2[:,:ow]=True
                    if y>0: mask2[:oh,:]=True
                    cop = cost.copy(); cop[~mask2]=np.inf
                    m=cut(cop)
                    best=(cand.copy(),score,m.copy())

            best_patch,best_score,best_mask = best
            old = result[y:y+ry, x:x+rx].copy()
            mask2 = np.zeros((ry,rx),bool)
            if x>0: mask2[:,:ow]=True
            if y>0: mask2[:oh,:]=True
            res = old.copy()
            res[~mask2] = best_patch[~mask2]
            res[mask2&best_mask] = best_patch[mask2&best_mask]
            result[y:y+ry, x:x+rx] = res
    return result