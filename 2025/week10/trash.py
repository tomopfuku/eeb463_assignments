def stasis_MCMC(gen,thin,start_p,bias_prior,sigma_prior,bias_prop,sigma_prop):
    bias = start_p[0]
    sigma = start_p[1]
    ll = stasis_ts_ll(bias,sigma,times,pheno) + bias_prior.log_pdf(bias) + sigma_prior.log_pdf(sigma)
    
    bias_samp = [bias]
    sigma_samp = [sigma]
    gens = [0]
    accept = 0

    for i in range(gen):

        if random.random() < .5:                   ## half the time we update bias, the other half sigma
            bias_star = bias + bias_prop.sample(1)[0]
            sigma_star = sigma
        else:
            bias_star = bias
            sigma_star = generate_sigma_proposal(sigma,sigma_prop)

        ll_star = stasis_ts_ll(bias_star,sigma_star,times,pheno) + bias_prior.log_pdf(bias_star) + sigma_prior.log_pdf(sigma_star)
        if ll_star - ll > 0.:
            ratio = 1.1
        else:
            ratio = math.exp(ll_star - ll)
        if random.random() < ratio:
            accept+=1
            ll = ll_star
            bias = bias_star
            sigma = sigma_star

        if i % thin == 0:
            gens.append(i)
            bias_samp.append(bias)
            sigma_samp.append(sigma)
    
    print("MCMC complete. Acceptance ratio:",accept / gen)
    return gens,bias_samp,sigma_samp
    
            
