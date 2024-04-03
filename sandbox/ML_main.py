import warnings

from wnews.NewsSite.APIparsers.ApiModels import ArticleTagsEnum
from wnews.NewsSite.MachineLearning.SvmLib import SvmManager
from wnews.NewsSite.MachineLearning.TextManager import TextManager


def main():
    warnings.filterwarnings('ignore')
    text_manager = TextManager()

    manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.economy, ArticleTagsEnum.science,
                         ArticleTagsEnum.musics, ArticleTagsEnum.films, ArticleTagsEnum.politics)

    manager.load_all_svm_states()
    manager_dicts = manager.load_add_svm_dicts()

    print()
    print("Politics dictionary:")

    for word in manager_dicts[5]:
        print(word)

    #print(len(manager_dicts))

    #articles = text_manager.get_new_articles(ArticleTagsEnum.all)
    #print(len(articles))
    #for article in articles:
    #    print(manager.predict_article(article.full_text, manager_dicts).name)

    '''
    articles, texts = text_manager.get_articles(ArticleTagsEnum.sport, 10)

    print()
    print(articles[0].title)
    print(articles[0].text)
    print(articles[0].article_link)
    print(articles[0].image_link)
    print(articles[0].last_update)
    '''
    '''
    test_artiles_cnt = 2400
    val_articles_cnt = 100
    dict_len = 1200

    c_arr = np.arange(0.1, 1000, 100)
    #c_arr = [100]
    sigma_arr = [0.0209, 0.0023, 0.0082, 0.0167, 0.0182, 0.0137]#np.arange(0.0001, 0.01, 0.0001) #[0.0209 0.0023 0.0082 0.0167 0.0182 0.0137]

    x, y = manager.get_train_data(test_artiles_cnt, dict_len, shift_articles=2000, save=False, dicts=manager_dicts)

    manager.check_train_adapters(x, y)
    print("Best Precision:", manager._precision_vector)
    print("Best C vector:", manager._c_vector)
    print("Best Sigma vector:", manager._sigma_vector)
    #manager.train_adapters(x, y, 100, sigma_arr)
    #manager.save_all_states()
    '''
    '''
    x_val, y_val = manager.get_train_data(val_articles_cnt + test_artiles_cnt, dict_len, test_artiles_cnt)

    print("Xval, yval shape", x_val.shape, y_val.shape)

    for c in c_arr:
        for sigma in sigma_arr:
            manager.train_adapters(x, y, c, sigma)
            manager.check_train_adapters(x_val, y_val)
            print("Sigma:", sigma, "Coef:", c)
            print("Best Precision:", manager._precision_vector)
            print("Best C vector:", manager._c_vector)
            print("Best Sigma vector:", manager._sigma_vector)

    for c, sigma in zip(manager._c_vector, manager._sigma_vector):
        manager.train_adapters(x, y, c, sigma)

    #manager.save_all_states()
    '''
    print("Finish")


if __name__ == '__main__':
    main()
