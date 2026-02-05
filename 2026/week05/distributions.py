from random import random
import math

def mean(vals):
    addup=0.0
    for i in vals:
        addup += i
    return addup / float(len(vals))

def std(vals):
    m = mean(vals)
    diffsum = 0.0
    for i in vals:
        diffsum += (i-m) ** 2.0
    s = math.sqrt( diffsum / float(len(vals)) )
    return s

class uniform:
    def __init__(self, lower=0.0, upper=1.0):
        self.upper = upper
        self.lower = lower

    def random_vec(self, n=1):
        vals = []
        for i in range(n):
            x = random()
            rval = lower + (x * (upper-lower))
            vals.append(rval)
        return vals

    def random_float(self):
        x = random()
        rval = self.lower + (x * (self.upper-self.lower))
        return rval

class normal:
    def __init__(self, mean = 0.0, sd = 1.0):
        self.mean = mean
        self.sd = sd

    def random_vec(self, n=1, method="box_muller"):
        norm=[]
        while True:
            if len(norm) == n:
                break
            if len(norm) > n:
                norm = norm[0:n]
                break

            # this is what we will use in class
            if method == "box_muller":
                x = random()
                y = random()
                xnorm = (((math.sqrt(-2 * math.log(x)) * math.cos(2. * math.pi * y))*self.sd)+self.mean)
                ynorm = (((math.sqrt(-2 * math.log(x)) * math.sin(2. * math.pi * y))*self.sd)+self.mean)
                norm.append(xnorm)
                norm.append(ynorm)
                #print(xnorm)
                #print(ynorm)

            # this is another approach for doing this that i am leaving because it is cool
            elif method == "polar":
                unif = uniform(-1.0,1.0)
                while True:
                    x = unif.random_float()
                    y = unif.random_float()
                    s = (x ** 2) + (y ** 2)
                    if s > 0 and s < 1:
                        break
                xnorm = (((x/math.sqrt(s))*math.sqrt(-2*math.log(s)))*self.sd)+self.mean
                ynorm = (((y/math.sqrt(s))*math.sqrt(-2*math.log(s)))*self.sd)+self.mean
                norm.append(xnorm)
                norm.append(ynorm)
        return norm

    def pdf(self, x):
        dens = (1.0/(self.sd*math.sqrt(2*math.pi)))*(math.e ** (-.5 * (((x - self.mean)/self.sd)**2)))
        return dens
    # calculates the mean and stdev from a sample
    # and reassigns the parameters of the distribution
    def fit_mle(self, sample):
        self.mean = mean(sample)
        self.sd = std(sample)
        return

class binomial:
    def __init__(self,n,p):
        self.n = n
        self.p = p

    def random_vec(self,rep=1):
        res = []
        for i in range(rep):
            succ=0
            for j in range(self.n):
                r = random()
                if r < self.p:
                    succ += 1
            res.append(succ)
        return res

class exponential:
    def __init__(self,rate):
        self.rate = rate

    def random_vec(self, n=1):
        exp = []
        for rep in range(n):
            r = random()
            val = math.log(1-r)/(-self.rate)
            exp.append(val)
        return exp

def main():
    norm = normal(0, 10)
    #print(norm.random_vec(1000,"box_muller"))
    exp = exponential(2)
    print(exp.random_vec(2))

if __name__ == "__main__":
    main()
